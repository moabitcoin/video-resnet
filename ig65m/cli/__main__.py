import argparse
from pathlib import Path

import ig65m.cli.convert
import ig65m.cli.extract
import ig65m.cli.semcode
import ig65m.cli.dreamer
import ig65m.cli.vgan


parser = argparse.ArgumentParser(prog="ig65m")

subcmd = parser.add_subparsers(dest="command")
subcmd.required = True

Formatter = argparse.ArgumentDefaultsHelpFormatter


convert = subcmd.add_parser("convert", help="🍝 converts model weights", formatter_class=Formatter)
convert.add_argument("pkl", type=Path, help=".pkl file to read the R(2+1)D 34 layer weights from")
convert.add_argument("out", type=Path, help="prefix to save converted R(2+1)D 34 layer weights to")
convert.add_argument("--frames", type=int, choices=(8, 32), required=True, help="clip frames for video model")
convert.add_argument("--classes", type=int, choices=(359, 400, 487), required=True, help="classes in last layer")
convert.set_defaults(main=ig65m.cli.convert.main)


extract = subcmd.add_parser("extract", help="🍪 extracts video features", formatter_class=Formatter)
extract.add_argument("video", type=Path, help="video to run feature extraction on")
extract.add_argument("features", type=Path, help="file to save video features to")
extract.add_argument("--frame-size", type=int, default=128, help="size of smaller edge for frame resizing")
extract.add_argument("--batch-size", type=int, default=1, help="number of sequences per batch for inference")
extract.add_argument("--pool-spatial", type=str, choices=("mean", "max"), default="mean", help="spatial pooling")
extract.add_argument("--pool-temporal", type=str, choices=("mean", "max"), default="mean", help="temporal pooling")
extract.set_defaults(main=ig65m.cli.extract.main)


semcode = subcmd.add_parser("semcode", help="🔰 generates semantic codes", formatter_class=Formatter)
semcode.add_argument("features", type=Path, help="file to read video features from")
semcode.add_argument("image", type=Path, help="file to save semantic code image to")
semcode.add_argument("--color", type=int, default=20, help="HSV hue in angle [0, 360]")
semcode.set_defaults(main=ig65m.cli.semcode.main)


dreamer = subcmd.add_parser("dreamer", help="💤 dream of electric sheep", formatter_class=Formatter)
dreamer.add_argument("video", type=Path, help="video to plant into the dream")
dreamer.add_argument("dream", type=Path, help="file to save dream animation to")
dreamer.add_argument("--frame-size", type=int, default=128, help="size of smaller edge for frame resizing")
dreamer.add_argument("--lr", type=float, default=0.1, help="how lucid the dream is")
dreamer.add_argument("--num-epochs", type=int, default=100, help="how long to dream")
dreamer.add_argument("--gamma", type=float, default=1e-4, help="total variation regularization")
dreamer.set_defaults(main=ig65m.cli.dreamer.main)


vgan = subcmd.add_parser("vgan", help="🥑 video generative adversarial network", formatter_class=Formatter)
vgan.add_argument("videos", type=Path, help="directory to read videos from")
vgan.add_argument("--checkpoints", type=Path, required=True, help="directory to save checkpoints to")
vgan.add_argument("--num-epochs", type=int, default=100, help="number of epochs to run through dataset")
vgan.add_argument("--batch-size", type=int, default=1, help="number of clips per batch")
vgan.add_argument("--clip-length", type=int, default=32, help="number of frames per clip")
vgan.add_argument("--z-dimension", type=int, default=128, help="noise dimensionality")
vgan.add_argument("--save-frequency", type=int, default=100, help="number of steps to checkpoint after")
vgan.add_argument("--logs", type=Path, required=True, help="directory to save TensorBoard logs to")
vgan.set_defaults(main=ig65m.cli.vgan.main)


args = parser.parse_args()
args.main(args)
