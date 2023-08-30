from typing import Tuple


def publish_args(branch_name) -> Tuple[str, str]:
    return (
        "https://github.com/blooop/phase_change_mug.git",
        f"https://github.com/blooop/phase_change_mug/blob/{branch_name}",
    )
