# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Rigging Toolkit",
    "description": "A series of tools for rigging in Blender.",
    "author": "Frederick Solano | Afternoon Circus",
    "version": (0, 0),
    "blender": (4, 0, 2),
    "location": "3D View > Rigging Toolkit",
    "warning": "In Development",  # used for warning icon and text in addons panel
    "doc_url": "https://github.com/afternooncircus/Blender_rigging_toolkit",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "Rigging",
}

from .ui import register_ui, unregister_ui
from .operators import register_operators, unregister_operators


def register() -> None:
    register_ui()
    register_operators()


def unregister() -> None:
    unregister_ui()
    unregister_operators()
