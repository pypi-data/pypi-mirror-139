# Copyright 2022 Soul Machines Ltd

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utility functions for working with memory arrays"""
from typing import Any, Dict, List, Tuple, Union

from smskillsdk.models.api import Memory


def serialize_memory(data: dict, session_id: Union[str, None] = None) -> List[Memory]:
    """Convert a Python dict into a list of Memory objects

    Key-value pairs will be converted into objects with these properties

    {
        "name": <key: Any>,
        "value": <value: Any>
        "session_id": <session_id: str> (optional)
    }
    """
    memory = list()
    for key, value in data.items():
        if session_id is None:
            memory.append(Memory(**{"name": key, "value": value}))
        else:
            memory.append(
                Memory(**{"name": key, "value": value, "session_id": session_id})
            )

    return memory


def deserialize_memory(
    memories: List[Memory], session_id: Union[str, None] = None
) -> Dict[str, Any]:
    """Convert a list of memory objects to a dictionary

    It is assumed memory objects will have name/value attributes. If multiple memory
    objects share the same name values, the latest value in the list will be used. If
    a session_id is provided, this will be checked and used to filter out memories
    without a matching session_id.
    """
    result = dict()
    for memory in memories:
        if isinstance(memory, Memory):
            if session_id is not None and (
                not hasattr(memory, "session_id") or memory.session_id != session_id
            ):
                continue

            if hasattr(memory, "name") and hasattr(memory, "value"):
                result[memory.name] = memory.value

    return result


def get_memory_value(
    memories: List[Memory], key: str, session_id: Union[str, None] = None
) -> Tuple[bool, Any]:
    """Gets a value from the memory array corresponding to an optional session_id"""
    for memory in memories:
        if isinstance(memory, Memory):
            if session_id is not None and (
                not hasattr(memory, "session_id") or memory.session_id != session_id
            ):
                continue

            if (
                hasattr(memory, "name")
                and hasattr(memory, "value")
                and memory.name == key
            ):

                return True, memory.value

    return False, None


def set_memory_value(
    memories: List[Memory], key: str, value: Any, session_id: Union[str, None] = None
) -> None:
    """Sets a value in the memory array corresponding to an optional session_id"""
    found = False

    for memory in memories:
        if isinstance(memory, Memory):
            if session_id is not None and (
                not hasattr(memory, "session_id") or memory.session_id != session_id
            ):
                continue

            if (
                hasattr(memory, "name")
                and hasattr(memory, "value")
                and memory.name == key
            ):
                memory.value = value
                found = True

    if not found:
        if session_id is None:
            memories.append(Memory(**{"name": key, "value": value}))
        else:
            memories.append(
                Memory(**{"name": key, "value": value, "session_id": session_id})
            )
