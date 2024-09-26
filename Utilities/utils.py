import os
import struct
import io
import zipfile
import enum
import shutil
from typing import List

class EndianType(enum.Enum):
    BigEndian = 'big'
    LittleEndian = 'little'

class Utilities:
    imgStandardIcon = bytes([
        137, 80, 78, 71, 13, 10, 26, 10, 0, 0, 0, 13, 73, 72, 68, 82,
        0, 0, 0, 48, 0, 0, 0, 48, 8, 6, 0, 0, 0, 87, 2, 249,
        135, 0, 0, 3, 197, 73, 68, 65, 84, 120, 156, 237, 89, 221, 106,
        19, 65, 20, 254, 102, 119, 147, 108, 154, 100, 211, 38, 80, 44, 197,
        187, 233, 69, 75, 107, 161, 125, 8, 91, 161, 72, 138, 32, 237, 165,
        87, 94, 8, 245, 194, 7, 40, 189, 108, 133, 84, 47, 244, 9, 132,
        130, 248, 0, 190, 129, 149, 234, 69, 177, 80, 65, 42, 70, 40, 168,
        40, 165, 197, 152, 253, 153, 227, 197, 54, 109, 154, 100, 51, 51, 187,
        211, 170, 208, 15, 6, 118, 119, 206, 206, 249, 206, 156, 159, 153, 157,
        5, 46, 113, 137, 75, 252, 183, 96, 34, 129, 157, 157, 157, 29, 223,
        48, 12, 131, 115, 206, 181, 41, 237, 203, 57, 216, 255, 242, 250, 213,
        194, 226, 189, 135, 123, 159, 190, 190, 79, 50, 150, 37, 18, 8, 130,
        192, 28, 30, 30, 30, 134, 239, 251, 73, 244, 156, 128, 136, 144, 74,
        219, 8, 220, 145, 27, 149, 202, 157, 95, 143, 159, 60, 189, 239, 121,
        222, 190, 150, 193, 187, 97, 123, 123, 155, 136, 136, 136, 56, 143, 104,
        68, 68, 20, 16, 15, 196, 141, 56, 167, 70, 163, 65, 245, 122, 157,
        190, 127, 251, 65, 31, 118, 119, 169, 90, 173, 190, 201, 100, 50, 153,
        107, 199, 234, 132, 17, 209, 14, 195, 144, 21, 228, 156, 71, 52, 31,
        129, 31, 213, 119, 182, 205, 247, 125, 4, 65, 0, 223, 247, 209, 151,
        183, 241, 185, 86, 195, 204, 204, 204, 116, 181, 90, 125, 105, 219, 246,
        24, 0, 58, 55, 3, 186, 131, 64, 210, 42, 9, 140, 1, 150, 105,
        193, 52, 77, 100, 237, 44, 92, 215, 5, 99, 12, 183, 230, 230, 198,
        151, 151, 151, 159, 231, 243, 249, 249, 49, 85, 6, 49, 13, 32, 16,
        201, 146, 39, 52, 39, 150, 8, 161, 17, 150, 117, 124, 79, 200, 102,
        179, 72, 101, 50, 88, 92, 88, 152, 90, 91, 91, 219, 40, 20, 10,
        227, 42, 76, 98, 24, 160, 54, 235, 64, 72, 188, 245, 157, 102, 160,
        51, 198, 224, 56, 14, 74, 165, 18, 50, 182, 141, 74, 165, 50, 246,
        104, 117, 245, 69, 177, 88, 156, 132, 100, 62, 40, 27, 16, 135, 124,
        20, 130, 32, 0, 0, 184, 174, 11, 199, 113, 144, 74, 165, 80, 153,
        159, 159, 145, 149, 149, 149, 141, 66, 161, 48, 37, 163, 69, 88, 70,
        91, 9, 233, 36, 15, 0, 144, 78, 165, 241, 118, 107, 11, 5, 199,
        129, 239, 251, 224, 156, 195, 117, 93, 220, 156, 157, 29, 169, 213, 106,
        207, 214, 215, 215, 111, 187, 174, 187, 215, 107, 12, 105, 15, 168, 196,
        123, 123, 200, 116, 149, 225, 28, 83, 211, 211, 24, 26, 186, 130, 92,
        46, 135, 254, 98, 17, 197, 129, 1, 12, 14, 14, 194, 48, 77, 60,
        88, 90, 154, 154, 156, 156, 188, 11, 32, 221, 75, 163, 130, 7, 100,
        200, 139, 12, 61, 237, 116, 60, 207, 67, 185, 92, 9, 229, 114, 169,
        67, 234, 112, 244, 232, 8, 133, 124, 30, 163, 163, 163, 19, 155, 155,
        155, 87, 1, 124, 140, 26, 81, 131, 1, 167, 164, 122, 207, 122, 203,
        29, 133, 9, 236, 54, 26, 103, 250, 25, 0, 142, 176, 15, 0, 130,
        32, 168, 119, 188, 220, 134, 132, 6, 168, 205, 122, 187, 92, 72, 148,
        208, 90, 112, 12, 0, 150, 105, 134, 242, 156, 91, 34, 142, 9, 12,
        72, 70, 190, 189, 191, 85, 198, 56, 246, 0, 1, 38, 194, 198, 58,
        132, 143, 17, 195, 128, 120, 33, 163, 38, 115, 114, 35, 220, 2, 199,
        242, 128, 108, 57, 141, 111, 32, 181, 94, 232, 204, 1, 153, 181, 64,
        20, 90, 74, 97, 37, 52, 64, 97, 37, 150, 153, 118, 173, 228, 165,
        32, 237, 1, 157, 164, 34, 226, 93, 66, 87, 39, 180, 148, 209, 104,
        165, 210, 177, 46, 144, 139, 70, 76, 3, 212, 137, 169, 200, 168, 124,
        150, 157, 83, 25, 109, 123, 67, 217, 64, 121, 23, 40, 237, 70, 163,
        9, 201, 200, 196, 243, 138, 8, 202, 30, 208, 21, 235, 113, 103, 188,
        29, 74, 31, 52, 58, 19, 85, 190, 191, 55, 18, 150, 209, 243, 157,
        121, 153, 100, 78, 148, 196, 39, 79, 52, 18, 39, 234, 58, 96, 36,
        18, 173, 3, 186, 67, 170, 41, 171, 18, 84, 177, 170, 80, 171, 178,
        168, 254, 78, 25, 49, 241, 56, 249, 32, 145, 196, 157, 251, 169, 127,
        133, 60, 160, 229, 88, 229, 239, 145, 7, 20, 115, 64, 134, 216, 69,
        146, 7, 98, 151, 81, 17, 249, 222, 164, 66, 185, 100, 196, 155, 16,
        135, 80, 71, 10, 36, 219, 65, 170, 236, 52, 101, 32, 225, 129, 222,
        203, 73, 188, 45, 178, 62, 43, 36, 67, 72, 84, 137, 244, 197, 122,
        120, 170, 167, 117, 33, 139, 249, 81, 114, 166, 75, 158, 188, 170, 119
    ])

class Utils:
    @staticmethod
    def hex2binary(hex_str: str) -> bytes:
        return bytes.fromhex(hex_str)

    @staticmethod
    def hex_to_dec(hex_bytes: bytes, reverse: str = "") -> int:
        if reverse == "reverse":
            hex_bytes = hex_bytes[::-1]
        return int.from_bytes(hex_bytes, byteorder='big')

    @staticmethod
    def read_write_data(file_to_use: str, file_to_use2: str = "", method_read_or_write_or_both: str = "", method_binary_or_integer: str = "", bin_data: bytes = None, bin_data2: int = 0, offset: int = 0, count: int = 0):
        if method_read_or_write_or_both == "r":
            with open(file_to_use, 'rb') as f:
                read_buffer = f.read()
            return read_buffer
        elif method_read_or_write_or_both == "w":
            with open(file_to_use, 'ab') as f:
                if method_binary_or_integer == "bi":
                    f.write(bin_data)
                elif method_binary_or_integer == "in":
                    f.write(struct.pack('i', bin_data2))
        elif method_read_or_write_or_both == "b":
            with open(file_to_use, 'rb') as fr, open(file_to_use2, 'ab') as fw:
                fr.seek(offset)
                buffer_size = 4096
                while count > 0:
                    buffer = fr.read(min(buffer_size, count))
                    if not buffer:
                        break
                    fw.write(buffer)
                    count -= len(buffer)

    @staticmethod
    def compare_bytes(a: bytes, b: bytes) -> bool:
        return a == b

    @staticmethod
    def extract_file_to_directory(zip_file_name: str, output_directory: str):
        with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
            zip_ref.extractall(output_directory)

    @staticmethod
    def byte_to_string(buff: bytes) -> str:
        return buff.hex().upper()

    @staticmethod
    def generate_stream_from_string(s: str) -> io.BytesIO:
        return io.BytesIO(s.encode())

    @staticmethod
    def read_uint32(stream: io.BytesIO) -> int:
        return struct.unpack('<I', stream.read(4))[0]

    @staticmethod
    def read_uint16(stream: io.BytesIO) -> int:
        return struct.unpack('<H', stream.read(2))[0]

    @staticmethod
    def read_ascii_string(stream: io.BytesIO, length: int) -> str:
        return stream.read(length).decode('ascii')

    @staticmethod
    def read_utf8_string(stream: io.BytesIO, length: int) -> str:
        return stream.read(length).decode('utf-8')

    @staticmethod
    def read_byte(stream: io.BytesIO, length: int) -> bytes:
        return stream.read(length)