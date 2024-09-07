#ifndef GBN_BUFFER_H
#define GBN_BUFFER_H

#include <stdbool.h>

/* a packet is the data unit passed from layer 4 (students code) to layer */
/* 3 (teachers code).  Note the pre-defined packet structure, which all   */
/* students must follow. */
struct pkt {
   int seqnum;
   int acknum;
   int checksum;
   char payload[20];
    };

// stores packets to be sent
typedef struct Buffer
{
	struct pkt packets[50];			// size of buffer - 50 packets
	int start;
	int size;
} Buffer;

Buffer buffer; 

void initBuffer()
{
	buffer.start = 0;
	buffer.size = 0;
}

bool isBufferFull()
{
	return buffer.size == 50;
}

bool isBufferEmpty()
{
	return buffer.size == 0;
}

void addPktToBuffer(struct pkt packet)
{
	int newPacketIndex = (buffer.start + buffer.size) % 50;
	buffer.packets[newPacketIndex] = packet;
	buffer.size++;
	printf("addPktToBuffer: %s\n", packet.payload);
}

struct pkt getPktFromBuffer()
{
	struct pkt packet = buffer.packets[buffer.start];
	printf("getPktFromBuffer: %s\n", packet.payload);
	buffer.start = (buffer.start + 1) % 50;
	buffer.size--;
	return packet;
}

#endif 	// GBN_BUFFER_H