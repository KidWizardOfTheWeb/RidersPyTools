from pathlib import Path

def check_types(read_data_type):
    increment = 0
    match read_data_type:
        case 'u8' | 's8':
            increment = 1
        case 'bool':
            increment = 1
            read_data_type = "Bool"
        case 'u16' | 's16':
            increment = 2
        case 'u32' | 's32':
            increment = 4
        case 'f32':
            increment = 4
        case 'u64' | 's64':
            increment = 8
        case _:
            print("Special case found: ", read_data_type)

            # Get interpreted types possibly.
            special_type = read_data_type[read_data_type.index("<") + 1:read_data_type.index(">")]
            flag_mapping = str.maketrans({"<": "(\"", ">": "\")"})
            filler_mapping = str.maketrans({"<": "(", ">": ")"})
            # Attempt to detect Flags
            if "Flag" in read_data_type:
                new_type_name = read_data_type.translate(flag_mapping)
                # Check for specific flag instances here.
                if special_type == "Buttons":
                    return 4, new_type_name
                pass
            if "fillerData" in read_data_type:
                new_filler_name = read_data_type.translate(filler_mapping)
                # Return value
                return int(special_type, 16), new_filler_name

            # Otherwise, give it a size
            new_type = int(input("Give a new length: "))
            increment = new_type


    return increment, read_data_type

def parse(struct_lines):
    # Read in raw struct data, make a string so I can copy it later
    offset_val = 0
    final_output = ""
    for line in struct_lines:
        # Get the segments we need:
        # Type
        # Name
        # Arrays mess this up sometimes
        line_segments = line.split()
        ptr_string = ""
        # TODO: This is probably an array or some other exception, handle differently
        if len(line_segments) > 2:
            type = line_segments[0] + line_segments[1]
            var_name = line_segments[2]
            var_name = var_name.replace(";", "")
            # offset_val += 4
            return
        else:
            type = line_segments[0]
            var_name = line_segments[1]

        var_name = var_name.replace(";", "")
        if "*" in var_name:
            # this is a ptr, handle specially
            var_name = var_name.replace("*", "")
            ptr_string = ", " + "None"

        increment, interpreted_type = check_types(type)
        print_str = "super().__setattr__('" + var_name + "', " + "OffsetAttr(ptr_start_addr + " + str(hex(offset_val)) + ", " + str(interpreted_type) + ptr_string + "))"
        offset_val += increment

        final_output = final_output + "\n" + print_str

    return final_output


if __name__ == '__main__':
    # struct_str = input()
    # struct_list = struct_str.split("\n")

    # Check other text files for ref on format
    # Change path here
    with open(Path("C:/Users/XYZ/Documents/RidersPyTools/structText/GearStats"), "r") as file:
        struct_lines = file.readlines()
        print(parse(struct_lines))
        pass


