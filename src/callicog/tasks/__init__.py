import os
import pathlib


_this_dir = pathlib.Path(__file__).parent.resolve()
IMAGE_DIR = os.environ.get("CALLICOG_TASK_IMAGE_DIR") or _this_dir/"images"


if __name__ == "__main__":
    # TODO delete this after troubleshooting the .env situation.
    print(IMAGE_DIR)
    import pdb; pdb.set_trace()
