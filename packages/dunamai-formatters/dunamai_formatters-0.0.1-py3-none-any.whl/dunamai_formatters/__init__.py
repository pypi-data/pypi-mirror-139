"""A complementary tool to Dunamai that offers formatters that can be used as the format argument of the serialize function."""  # noqa: E501
import dunamai as _dunamai

from . import pep440

__app_name__ = "dunamai-formatters"
__version__ = _dunamai.get_version(
    __app_name__, third_choice=_dunamai.Version.from_any_vcs, ignore=[_dunamai.Version("0")]
).serialize(format=pep440.meta_id)
