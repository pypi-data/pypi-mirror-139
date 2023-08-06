"""Formatters based on PEP 440."""
from dunamai import Version

from dunamai_formatters.helpers import format_pieces_as_pep440


def pep440(version: Version) -> str:
    """
    Serialize a version based on PEP 440. (e.g. 0.1.0a8.post3+gf001c3f.dirty.linux).
    Use this with `Version.serialize()` if you want more control
    over how the version is mapped.

    :param version: The version.
    :return: Serialized version.
    """
    if version.commit:
        if version.tagged_metadata:
            metadata = [version.commit, version.tagged_metadata]
        else:
            metadata = [version.commit]
    else:
        metadata = None
    return format_pieces_as_pep440(
        version.base,
        stage=version.stage,
        revision=version.revision,
        post=version.distance,
        epoch=version.epoch,
        metadata=metadata,
    )


def base(version: Version) -> str:
    """
    Serialize a version based on PEP 440, but remove the distance and the
    metadata. (e.g. 0.1.0a8).
    Use this with `Version.serialize()` if you want more control
    over how the version is mapped.

    :param version: The version.
    :return: Serialized version.
    """
    return format_pieces_as_pep440(
        version.base,
        stage=version.stage,
        revision=version.revision,
        epoch=version.epoch,
    )


def meta(version: Version) -> str:
    """
    Serialize a version based on PEP 440, with the distance and commit in the
    metadata. (e.g. 0.1.0a8+3.f001c3f.dirty.linux).
    Use this with `Version.serialize()` if you want more control
    over how the version is mapped.

    :param version: The version.
    :return: Serialized version.
    """
    metadata = []
    if version.distance:
        metadata.extend([f"{version.distance}", f"{version.commit}"])
    if version.dirty:
        metadata.append("dirty")
    if version.tagged_metadata:
        filter_list = [version.distance, version.commit, "dirty"]
        metadata.extend([m for m in [e.strip() for e in version.tagged_metadata.split(".")] if m not in filter_list])
    return format_pieces_as_pep440(
        version.base,
        stage=version.stage,
        revision=version.revision,
        epoch=version.epoch,
        metadata=metadata,
    )


def meta_id(version: Version) -> str:
    """
    Serialize a version based on PEP 440, with the distance and commit in the
    metadata. The distance and commit are preceded by an identifier. (e.g. 0.1.0a8+d3.gf001c3f.dirty.linux).
    Use this with `Version.serialize()` if you want more control
    over how the version is mapped.

    :param version: The version.
    :return: Serialized version.
    """
    metadata = []
    if version.distance:
        metadata.extend([f"d{version.distance}", f"g{version.commit}"])
    if version.dirty:
        metadata.append("dirty")
    if version.tagged_metadata:
        filter_list = [
            version.distance,
            f"d{version.distance}",
            version.commit,
            f"g{version.commit}",
            "dirty",
        ]
        metadata.extend([m for m in [e.strip() for e in version.tagged_metadata.split(".")] if m not in filter_list])
    return format_pieces_as_pep440(
        version.base,
        stage=version.stage,
        revision=version.revision,
        epoch=version.epoch,
        metadata=metadata,
    )
