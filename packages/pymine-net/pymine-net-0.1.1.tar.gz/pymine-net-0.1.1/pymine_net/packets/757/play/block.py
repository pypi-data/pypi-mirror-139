"""Contains packets related to blocks."""

from __future__ import annotations

from typing import List, Tuple

import pymine_net.types.nbt as nbt
from pymine_net.types.buffer import Buffer
from pymine_net.types.packet import ClientBoundPacket, ServerBoundPacket

__all__ = (
    "PlayBlockAction",
    "PlayBlockChange",
    "PlayQueryBlockNBT",
    "PlayPlayerBlockPlacement",
    "PlayNBTQueryResponse",
    "PlayMultiBlockChange",
)


class PlayBlockAction(ClientBoundPacket):
    """This packet is used for a number of actions and animations performed by blocks. (Server -> Client)

    :param int x: The x coordinate of the location where this occurs.
    :param int y: The y coordinate of the location where this occurs.
    :param int z: The z coordinate of the location where this occurs.
    :param int action_id: Block action ID, see here: https://wiki.vg/Block_Actions.
    :param int action_param: Action param of the action, see here: https://wiki.vg/Block_Actions.
    :param int block_type: The type of block which the action is for.
    :ivar int id: Unique packet ID.
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar action_id:
    :ivar action_param:
    :ivar block_type:
    """

    id = 0x0B

    def __init__(self, x: int, y: int, z: int, action_id: int, action_param: int, block_type: int):
        super().__init__()

        self.x, self.y, self.z = x, y, z
        self.action_id = action_id
        self.action_param = action_param
        self.block_type = block_type

    def pack(self) -> Buffer:
        return (
            Buffer()
            .write_position(self.x, self.y, self.z)
            .write("B", self.action_id)
            .write("B", self.action_param)
            .write_varint(self.block_type)
        )


class PlayBlockChange(ClientBoundPacket):
    """Fired when a block is changed within the render distance. (Server -> Client)

    :param int x: The x coordinate of the location where this occurs.
    :param int y: The y coordinate of the location where this occurs.
    :param int z: The z coordinate of the location where this occurs.
    :param int block_id: Block ID of what to change the block to.
    :ivar int id: Unique packet ID.
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar block_id:
    """

    id = 0x0C

    def __init__(self, x: int, y: int, z: int, block_id: int):
        super().__init__()

        self.x, self.y, self.z = x, y, z
        self.block_id = block_id

    def pack(self) -> Buffer:
        return Buffer().write_position(self.x, self.y, self.z).write_varint(self.block_id)


class PlayQueryBlockNBT(ServerBoundPacket):
    """Used when SHIFT+F3+I is used on a block. (Client -> Server)

    :param int transaction_id: Number used to verify that a response matches.
    :param int x: The x coordinate of the block.
    :param int y: The y coordinate of the block.
    :param int z: The z coordinate of the block.
    :ivar int id: Unique packet ID.
    :ivar transaction_id:
    :ivar x:
    :ivar y:
    :ivar z:
    """

    id = 0x01

    def __init__(self, transaction_id: int, x: int, y: int, z: int):
        super().__init__()

        self.transaction_id = transaction_id
        self.x, self.y, self.z = x, y, z

    @classmethod
    def unpack(cls, buf: Buffer) -> PlayQueryBlockNBT:
        return cls(buf.read_varint(), *buf.read_position())


class PlayPlayerBlockPlacement(ServerBoundPacket):
    """Sent by the client when it places a block. (Client -> Server)

    :param int hand: The hand used, either main hand (0), or offhand (1).
    :param int x: The x coordinate of the block.
    :param int y: The y coordinate of the block.
    :param int z: The z coordinate of the block.
    :param int face: The face of the block, see here: https://wiki.vg/Protocol#Player_Block_Placement.
    :param float cur_pos_x: The x position of the crosshair on the block.
    :param float cur_pos_y: The y position of the crosshair on the block.
    :param float cur_pos_z: The z position of the crosshair on the block.
    :param bool inside_block: True if the player's head is inside the block.
    :ivar int id: Unique packet ID.
    :ivar hand:
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar face:
    :ivar cur_pos_x:
    :ivar cur_pos_y:
    :ivar cur_pos_z:
    :ivar inside_block:
    """

    id = 0x2E

    def __init__(
        self,
        hand: int,
        x: int,
        y: int,
        z: int,
        face: int,
        cur_pos_x: float,
        cur_pos_y: float,
        cur_pos_z: float,
        inside_block: bool,
    ):
        super().__init__()

        self.hand = hand
        self.x, self.y, self.z = x, y, z
        self.face = face
        self.cur_pos_x = cur_pos_x
        self.cur_pos_y = cur_pos_y
        self.cur_pos_z = cur_pos_z
        self.inside_block = inside_block

    @classmethod
    def unpack(cls, buf: Buffer) -> PlayPlayerBlockPlacement:
        return cls(
            buf.read_varint(),
            *buf.read_position(),
            buf.read_varint(),
            buf.read("f"),
            buf.read("f"),
            buf.read("f"),
            buf.read("?"),
        )


class PlayNBTQueryResponse(ClientBoundPacket):
    """Sent by the client when it places a block. (Server -> Client)

    :param int transaction_id:
    :param nbt.TAG nbt_tag:
    :ivar int id: Unique packet ID.
    """

    id = 0x60

    def __init__(self, transaction_id: int, nbt_tag: nbt.TAG):
        super().__init__()

        self.transaction_id = transaction_id
        self.nbt_tag = nbt_tag

    def pack(self) -> Buffer:
        return Buffer().write_varint(self.transaction_id).write_nbt(self.nbt_tag)


class PlayMultiBlockChange(ClientBoundPacket):
    """Sent whenever 2 or more blocks change in the same chunk on the same tick. (Server -> Client)

    :param int chunk_sect_x: The x coordinate of the chunk section.
    :param int chunk_sect_y: The y coordinate of the chunk section.
    :param int chunk_sect_z: The z coordinate of the chunk section.
    :param bool trust_edges: The inverse of preceding PlayUpdateLight packet's trust_edges bool
    :param list blocks: The changed blocks, formatted like [block_id, local_x, local_y, local_z].
    :ivar int id: Unique packet ID.
    :ivar chunk_sect_x:
    :ivar chunk_sect_y:
    :ivar chunk_sect_z:
    :ivar trust_edges:
    :ivar blocks:
    """

    id = 0x3F

    def __init__(
        self,
        chunk_sect_x: int,
        chunk_sect_y: int,
        chunk_sect_z: int,
        trust_edges: bool,
        blocks: List[Tuple[int, int, int, int]],
    ):
        super().__init__()

        self.chunk_sect_x = chunk_sect_x
        self.chunk_sect_y = chunk_sect_y
        self.chunk_sect_z = chunk_sect_z
        self.trust_edges = trust_edges
        self.blocks = blocks

    def pack(self) -> Buffer:
        buf = (
            Buffer()
            .write_varint(
                ((self.chunk_sect_x & 0x3FFFFF) << 42)
                | (self.chunk_sect_y & 0xFFFFF)
                | ((self.chunk_sect_z & 0x3FFFFF) << 20)
            )
            .write("?", self.trust_edges)
            .write_varint(len(self.blocks))
        )

        for block_id, local_x, local_y, local_z in self.blocks:
            buf.write_varint(block_id << 12 | (local_x << 8 | local_z << 4 | local_y))

        return buf
