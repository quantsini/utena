#include <iostream>
#include <fstream>

using namespace std;

#pragma pack(push)
#pragma pack(1)

struct SCN_Header
{
    char file_type[4];
    int file_size;
    short start_data;
    short start_script;
    short unk1;
};

struct Text_Header
{
	unsigned char ptr_beg_1;
	unsigned short diag_ptr;
	unsigned short ptr_end_1;

	unsigned char ptr_beg_2;
	unsigned short tag_ptr;
	unsigned short ptr_end_2;

	unsigned char unk1;
	unsigned short unk2;
	unsigned char end_code;

	unsigned char zero;
};

#pragma pack(pop)

// Seperate function so as not to clutter up the main stuff
void PrintHeader(Text_Header current_line, ofstream &text)
{
	// Print off header

	text << "//";

	unsigned char bytes[255]; // more than enough for what we need

	sprintf((char*)bytes, "<$%02X>", current_line.ptr_beg_1);
	sprintf((char*)bytes + 0x05, "<$%04X>", current_line.diag_ptr);
	sprintf((char*)bytes + 0x0C, "<$%04X>", current_line.ptr_end_1);

	sprintf((char*)bytes + 0x13, "<$%02X>", current_line.ptr_beg_2);
	sprintf((char*)bytes + 0x18, "<$%04X>", current_line.tag_ptr);
	sprintf((char*)bytes + 0x1F, "<$%04X>", current_line.ptr_end_2);

	sprintf((char*)bytes + 0x26, "<$%02X>", current_line.unk1);
	sprintf((char*)bytes + 0x2B, "<$%02X>", current_line.unk2);
	sprintf((char*)bytes + 0x32, "<$%02X>", current_line.end_code);

	text << bytes;	

	text << "\n";
}

int main(int argc, char *argv[])
{

	if (argc < 4)
	{
		cout << "Usage : utena_extract.exe INPUT_FILE OUTPUT_FILE PTR_BLOCK_START\nNote: PTR_BLOCK_START must be in decimal format for now." << endl;
		return 0;
	}


	ifstream scn(argv[1], ios::binary);

	if (!scn.is_open())
	{
		return 0;
	}

	ofstream text(argv[2], ios::binary);

	unsigned int ptr_block_start = atoi(argv[3]);

	SCN_Header header;

	scn.read(reinterpret_cast<char*>(&header), sizeof(header));
	printf("file_type %s\n", header.file_type);
	printf("file_size %u\n", header.file_size);
	printf("start_data %u\n", header.start_data);
	printf("start_script %u\n", header.start_script);
	printf("unk1 %u\n", header.unk1);
	printf("*****************\n");

	// Get start of text
	scn.seekg(ptr_block_start, ios::beg);

	Text_Header current_line;
	scn.read(reinterpret_cast<char*>(&current_line), sizeof(current_line));

	printf("ptr_beg_1 %u\n", current_line.ptr_beg_1);
	printf("diag_ptr %u\n", current_line.diag_ptr);
	printf("ptr_end_1 %u\n", current_line.ptr_end_1);
	printf("ptr_beg_2 %u\n", current_line.ptr_beg_2);
	printf("tag_ptr %u\n", current_line.tag_ptr);
	printf("ptr_end_2 %u\n", current_line.ptr_end_2);
	printf("unk1 %u\n", current_line.unk1);
	printf("unkt2 %u\n", current_line.unk2);
	printf("end_code %u\n", current_line.end_code);
	printf("zero %u\n", current_line.zero);
	printf("%u\n", sizeof(current_line));

	// Lets extract the header script, no idea how it's used yet
	int script_size = current_line.tag_ptr - header.start_script;

	scn.seekg(header.start_script, ios::beg);

	while(scn.tellg() < header.start_script + script_size)
	{

		unsigned char byte = 0x00;
		scn.read(reinterpret_cast<char*>(&byte), 1);

		if (byte == 0x00)
		{
			//text << "\n\n";
		}
		else
		{
			//text.write(reinterpret_cast<char*>(&byte), 1);
		}

	}

	// DAY_A0 - 0x1E7F
	// DAY_A1 - 0x1A0E
	// DAY_B0 - 0x3628

	// Get start of text
	scn.seekg(ptr_block_start, ios::beg);

	scn.read(reinterpret_cast<char*>(&current_line), sizeof(current_line));

	// Output needed stuff for Atlas
	text << "#VAR(Table, TABLE)\n";
	text << "#ADDTBL(\"sjis.tbl\", Table)\n";
	text << "#ACTIVETBL(Table)\n";

	char cur_ptr[6];
	sprintf(cur_ptr, "%X", current_line.tag_ptr);

	text << "#JMP($";
	text.write(reinterpret_cast<char*>(&cur_ptr), 4);
	text << ")\n\n";

	Text_Header next_line;	
	int line_size;
	while(scn.tellg() <= header.start_script)
	{
		
		PrintHeader(current_line, text);

		int header_ptr = scn.tellg();
		text << "#W16($";

		
		sprintf(cur_ptr, "%04X", (short)(header_ptr - 9));

		text.write(reinterpret_cast<char*>(&cur_ptr), 4);

		text << ")\n";

		if (scn.tellg() < header.start_script)
		{
			scn.read(reinterpret_cast<char*>(&next_line), sizeof(next_line));
			line_size = (next_line.tag_ptr - current_line.tag_ptr) - 1;  // -1 to account for 0
		}
		else
		{
			scn.seekg(1, ios::cur); // Need to get past where were at so it'll exit
			line_size = (header.file_size - current_line.tag_ptr) - 1;
		}		

		unsigned char* line = new unsigned char[line_size];

		int cur_pos = scn.tellg();

		scn.seekg(current_line.tag_ptr, ios::beg);

		scn.read(reinterpret_cast<char*>(line), line_size);
		

		for(int i = 0; i < line_size; i++)
		{
			if (line[i] == 0)
			{

				text << "\n<$00>\n";

				text << "#W16($";

				char cur_ptr[6];
				sprintf(cur_ptr, "%04X", (short)(header_ptr - 14));

				text.write(reinterpret_cast<char*>(&cur_ptr), 4);

				text << ")\n\n//";
			}
			else if (line[i] == 0x0E)
			{
				text << "\\n\n//";
			}
			else
			{
				text.write(reinterpret_cast<char*>(&line[i]), 1);
			}
		}

	    text << "\n\n<$00>\n\n";

		delete[] line;


		current_line = next_line;

		scn.seekg(cur_pos, ios::beg);

	}

	scn.close();
	text.close();

	return 0;
}