
import argparse
import multiprocessing as mp

from pipeline import Pipeline
from streamer import Streamer
from viewer import Viewer
from detector import MotionDetector


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-path", type=str, default="People-6387.mp4",
                        help="Path to the input video file")
    args = parser.parse_args()

    pipeline = Pipeline(queue_size=10)

    pipeline.add_stage(Streamer(args.video_path))
    pipeline.add_stage(MotionDetector())
    pipeline.add_stage(Viewer())

    pipeline.run()


if __name__ == "__main__":
    mp.set_start_method("spawn")
    main()
