"""Helper functions to create different version formats."""
from typing import Sequence, Union


def format_pieces_as_pep440(  # pylint: disable=too-many-arguments
    base: str,
    stage: str = None,
    revision: int = None,
    post: int = None,
    dev: int = None,
    epoch: int = None,
    metadata: Sequence[Union[str, int]] = None,
) -> str:
    """
    Serialize a version based on PEP 440.
    Use this helper function to format the individual pieces into a format string.

    :param base: Release segment, such as 0.1.0.
    :param stage: Pre-release stage ("a", "b", or "rc").
    :param revision: Pre-release revision (e.g., 1 as in "rc1").
        This is ignored when `stage` is None.
    :param post: Post-release number.
    :param dev: Developmental release number.
    :param epoch: Epoch number.
    :param metadata: Any local version label segments.
    :return: Serialized version.
    """
    out = []  # type: list

    if epoch is not None:
        out.extend([epoch, "!"])

    out.append(base)

    if stage is not None:
        alternative_stages = {"alpha": "a", "beta": "b", "c": "rc", "pre": "rc", "preview": "rc"}
        out.append(alternative_stages.get(stage.lower(), stage.lower()))
        if revision is None:
            # PEP 440 does not allow omitting the revision, so assume 0.
            out.append(0)
        else:
            out.append(revision)

    if post is not None:
        out.extend([".post", post])

    if dev is not None:
        out.extend([".dev", dev])

    if metadata is not None and len(metadata) > 0:
        out.extend(["+", ".".join(map(str, metadata))])

    serialized = "".join(map(str, out))
    return serialized
