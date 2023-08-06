# Copyright (c) 2021 Sony Corporation. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
MSS Inference code using X-UMX/UMX.
'''

from pathlib import Path
import os
import warnings
from tqdm import trange
import norbert
import scipy.signal
import resampy
import soundfile as sf
import numpy as np
import nnabla as nn
from nnabla.ext_utils import get_extension_context
from pydub import AudioSegment
from pydub.utils import mediainfo
from .args import get_inference_args
from .model import *
from .utils import bandwidth_to_max_bin


def istft(X, rate=44100, n_fft=4096, n_hopsize=1024):
    _, audio = scipy.signal.istft(
        X / (n_fft // 2),
        rate,
        nperseg=n_fft,
        noverlap=n_fft - n_hopsize,
        boundary=True
    )
    return audio


def separate(audio, args):
    """
    Performing the separation on audio input
    Parameters
    ----------
    audio: np.ndarray [shape=(nb_timesteps, nb_channels)]
        mixture audio
    args : ArgumentParser
        ArgumentParser for OpenUnmix_CrossNet(X-UMX)/OpenUnmix(UMX) Inference

    Returns
    -------
    estimates: `dict` [`str`, `np.ndarray`]
        dictionary of all estimates as performed by the separation model.
    """

    # convert numpy audio to NNabla Variable
    audio_nn = nn.Variable.from_numpy_array(audio.T[None, ...])
    source_names = []
    V = []
    max_bin = bandwidth_to_max_bin(
        sample_rate=44100, n_fft=4096, bandwidth=16000)

    if not args.umx_infer:
        # Run X-UMX Inference
        nn.load_parameters(args.model)
        for j, target in enumerate(args.targets):
            if j == 0:
                unmix_target = OpenUnmix_CrossNet(
                    max_bin=max_bin, is_predict=True)
                mix_spec, msk, _ = unmix_target(audio_nn, test=True)
                # Network output is (nb_frames, nb_samples, nb_channels, nb_bins)
            V.append((msk[Ellipsis, j * 2:j * 2 + 2, :]
                      * mix_spec).d[:, 0, ...])
            source_names += [target]
    else:
        # Run UMX Inference
        for j, target in enumerate(args.targets):
            with nn.parameter_scope(target):
                unmix_target = OpenUnmix(max_bin=max_bin)
                nn.load_parameters(f"{os.path.join(args.model, target)}.h5")
                # Network output is (nb_frames, nb_samples, nb_channels, nb_bins)
                V.append(unmix_target(audio_nn, test=True).d[:, 0, ...])
            source_names += [target]

    V = np.transpose(np.array(V), (1, 3, 2, 0))
    if args.softmask:
        # only exponentiate the model if we use softmask
        V = V ** args.alpha

    real, imag = get_stft(audio_nn, center=True)

    # convert to complex numpy type
    X = real.d + imag.d * 1j
    X = X[0].transpose(2, 1, 0)

    if args.residual_model or len(args.targets) == 1:
        V = norbert.residual_model(V, X, args.alpha if args.softmask else 1)
        source_names += (['residual'] if len(args.targets) > 1
                         else ['accompaniment'])

    Y = norbert.wiener(V, X.astype(np.complex128), args.niter,
                       use_softmask=args.softmask)

    estimates = {}
    for j, name in enumerate(source_names):
        audio_hat = istft(
            Y[..., j].T,
            n_fft=unmix_target.n_fft,
            n_hopsize=unmix_target.n_hop
        )
        estimates[name] = audio_hat.T

    return estimates


def test():
    args = get_inference_args()

    # Set NNabla context and Dynamic graph execution
    ctx = get_extension_context(args.context)
    nn.set_default_context(ctx)

    # Enable the NNabla Dynamic excecution
    nn.set_auto_forward(True)

    for input_file in args.inputs:

        # get audio data from the path - all formats recognized by FFMPEG are recognized
        audio_with_meta = AudioSegment.from_file(input_file)
        sample_rate = int(mediainfo(input_file)['sample_rate'])
        channel_sounds = audio_with_meta.split_to_mono()
        samples = [s.get_array_of_samples()
                   for idx, s in enumerate(channel_sounds) if idx < 2]
        fp_arr = np.array(samples).T.astype(np.float32)
        fp_arr /= np.iinfo(samples[0].typecode).max
        audio = fp_arr

        if audio.shape[1] > 2:
            # if it is multi-channel audio, consider only first two channels
            warnings.warn(
                'Channel count > 2! '
                'Only the first two channels will be processed!')
            audio = audio[:, :2]

        if sample_rate != args.sample_rate:
            # resample to model samplerate if needed
            audio = resampy.resample(
                audio, sample_rate, args.sample_rate, axis=0)

        if audio.shape[1] == 1:
            # if we have mono, let's duplicate it
            # as the input of OpenUnmix is always stereo
            audio = np.repeat(audio, 2, axis=1)

        if args.chunk_dur is not None:
            # split and separate sources using moving window protocol for each chunk of audio
            # chunk duration must be lower for machines with low memory
            chunk_size = sample_rate * args.chunk_dur
            if (audio.shape[0] % chunk_size) == 0:
                nchunks = (audio.shape[0] // chunk_size)
            else:
                nchunks = (audio.shape[0] // chunk_size) + 1
        else:
            chunk_size = audio.shape[0]
            nchunks = 1

        estimates = {}
        for chunk_idx in trange(nchunks):
            cur_chunk = audio[chunk_idx *
                              chunk_size: min((chunk_idx + 1) * chunk_size, audio.shape[0]), :]
            cur_estimates = separate(cur_chunk, args)
            if any(estimates) is False:
                estimates = cur_estimates
            else:
                for key in cur_estimates:
                    estimates[key] = np.concatenate(
                        (estimates[key], cur_estimates[key]), axis=0)

        if not args.out_dir:
            model_path = Path(args.model)
            if not model_path.exists():
                output_path = Path(Path(input_file).stem + '_' + model)
            else:
                output_path = Path(
                    Path(input_file).stem + '_' + model_path.stem
                )
        else:
            if len(args.inputs) > 1:
                output_path = Path(args.out_dir) / Path(input_file).stem
            else:
                output_path = Path(args.out_dir)

        output_path.mkdir(exist_ok=True, parents=True)

        for target, estimate in estimates.items():
            sf.write(
                str(output_path / Path(target).with_suffix('.wav')),
                estimate,
                args.sample_rate
            )


if __name__ == '__main__':
    test()
