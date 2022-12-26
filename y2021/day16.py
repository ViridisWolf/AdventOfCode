#!/usr/bin/env python

from AdventOfCode import read_data


def day16():
    opcode_to_num = {
        'sum': 0,
        'product': 1,
        'min': 2,
        'max': 3,
        'literal': 4,
        'greater_than': 5,
        'less_than': 6,
        'equal_to': 7}
    opcode_from_num = {v: k for k, v in opcode_to_num.items()}

    def get_field(data, length, number=True):
        """ Get the next field in the packet.

        :param data: String of binary characters.
        :param length: Number of bits in the next field.
        :param number: The field will be converted to a number if True.
        :return: Tuple of the field bits/number and then the remaining data bits.
        """
        assert data
        field, data = data[:length], data[length:]
        if number:
            field = int(field, 2)
        return field, data

    def decode_packet(data):
        """
        Decode a bitstream into a packet.  Any un-decoded bitstream is also returned.
        :param data: The bitstream, as a string.
        :return: Tuple of dict and string.  {version:, type:, number, operate, subpackets}, remaining data
        """

        global version_sum
        result = {}
        version, data = get_field(data, 3)
        result['version'] = version
        version_sum += version
        pack_type, data = get_field(data, 3)
        pack_type = opcode_from_num[pack_type]
        result['type'] = pack_type

        if pack_type == 'literal':
            bits = ''
            cont = 1
            while cont:
                cont, data = get_field(data, 1)
                nybble, data = get_field(data, 4, number=False)
                bits += nybble
            number = int(bits, 2)
            result['number'] = number
        else:
            # Find and decode sub-packets.
            length_type, data = get_field(data, 1)
            result['length_type'] = length_type
            subs = []
            if length_type == 0:
                # Bits.
                bit_length, data = get_field(data, 15)
                result['sub_bits'] = bit_length
                sub_data, data = get_field(data, bit_length, number=False)
                while sub_data:
                    packet, sub_data = decode_packet(sub_data)
                    subs.append(packet)
            elif length_type == 1:
                # Counts.
                sub_count, data = get_field(data, 11)
                result['sub_count'] = sub_count
                for _ in range(sub_count):
                    packet, data = decode_packet(data)
                    subs.append(packet)
            else:
                raise
            result['subpackets'] = subs
        return result, data

    def do_opcode(packet):
        """ Perform the opcode and the values in the sub packets and return the resultant number. """
        # Prepare some values from the packet.
        opcode = packet['type']
        if 'subpackets' in packet:
            values = [do_opcode(p) for p in packet['subpackets']]

        # Perform instruction.
        if opcode == 'literal':
            return packet['number']
        elif opcode == 'sum':
            return sum(values)
        elif opcode == 'product':
            tmp = 1
            for val in values:
                tmp *= val
            return tmp
        elif opcode == 'min':
            return min(values)
        elif opcode == 'max':
            return max(values)
        elif opcode == 'greater_than':
            return int(values[0] > values[1])
        elif opcode == 'less_than':
            return int(values[0] < values[1])
        elif opcode == 'equal_to':
            return int(values[0] == values[1])
        else:
            raise AssertionError(f"Did not recognize opcode: {opcode}")
        raise

    # Done defining things, start doing.
    lines = read_data(__file__)
    data = ''
    for nybble in lines[0]:
        data += '{:04b}'.format(int(nybble, 16))

    global version_sum
    version_sum = 0
    outer_packet, _ = decode_packet(data)
    # print("Answer for 2021 day 16 part 1:", version_sum)
    # print("Answer for 2021 day 16 part 2:", do_opcode(outer_packet))
    return version_sum, do_opcode(outer_packet)


def main():
    return day16()


expected_answers = 1014, 1922490999789
