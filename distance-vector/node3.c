#include <stdio.h>
#include <stdbool.h>

extern struct rtpkt {
  int sourceid;       /* id of sending router sending this pkt */
  int destid;         /* id of router to which pkt being sent 
                         (must be an immediate neighbor) */
  int mincost[4];    /* min cost to node 0 ... 3 */
  };

extern int TRACE;
extern int YES;
extern int NO;

extern float clocktime;

struct distance_table 
{
  int costs[4][4];
} dt3;

/* students to write the following two routines, and maybe some others */

static void notifyNeighboringNodes()
{
	// Send the distance vector to 0 and 2 nodes:
	
	struct rtpkt updatePacket;
	updatePacket.sourceid = 3;
	for (int i = 0; i < 4; ++i)
	{
		updatePacket.mincost[i] = dt3.costs[i][3];
	}
	
	for (int i = 0; i < 4; ++i)
	{
		if (i == 1 || i == 3)
			continue;
		
		updatePacket.destid = i;
		tolayer2(updatePacket);
	}
}

void rtinit3() 
{
	// Initialize a distance vector:
	
	// destination 0:
	dt3.costs[0][0] = 7;
	dt3.costs[0][1] = 999;
	dt3.costs[0][2] = 999;
	dt3.costs[0][3] = 7;
	
	// destination 1:
	dt3.costs[1][0] = 999;
	dt3.costs[1][1] = 999;
	dt3.costs[1][2] = 999;
	dt3.costs[1][3] = 999;
	
	// destination 2:
	dt3.costs[2][0] = 999;
	dt3.costs[2][1] = 999;
	dt3.costs[2][2] = 2;
	dt3.costs[2][3] = 2;
	
	// destination 3:
	dt3.costs[3][0] = 999;
	dt3.costs[3][1] = 999;
	dt3.costs[3][2] = 999;
	dt3.costs[3][3] = 0;
	
	// printf("Node 3 initialization at %f\n\n", clocktime);
	
	printdt3(&dt3);
	
	notifyNeighboringNodes();
}


void rtupdate3(rcvdpkt)
  struct rtpkt *rcvdpkt;
  
{
	int srcNode = rcvdpkt->sourceid;
	
	// iterate over min costs of another node:
	
	printf("\nBefore update:\n");
	printdt3(&dt3);
	
	bool wasUpdated = false;
	for (int i = 0; i < 4; ++i)
	{
		if (dt3.costs[i][3] > rcvdpkt->mincost[i] + dt3.costs[srcNode][3])
		{
			dt3.costs[i][3] = rcvdpkt->mincost[i] + dt3.costs[srcNode][3];
			wasUpdated = true;
		}
	}
	
	// printf("Node 3 update at %f\n\n", clocktime);
	
	if (wasUpdated)
	{
		printf("\nAfter update:\n");
		printdt3(&dt3);
		
		printf("\nCosts to other nodes: 0 - %d, 1 - %d, 2 - %d\n", dt3.costs[0][3], dt3.costs[1][3], dt3.costs[2][3]);
		notifyNeighboringNodes();
	}
}


printdt3(dtptr)
  struct distance_table *dtptr;
  
{
  printf("             via     \n");
  printf("   D3 |    0     2 \n");
  printf("  ----|-----------\n");
  printf("     0|  %3d   %3d\n",dtptr->costs[0][0], dtptr->costs[0][2]);
  printf("dest 1|  %3d   %3d\n",dtptr->costs[1][0], dtptr->costs[1][2]);
  printf("     2|  %3d   %3d\n",dtptr->costs[2][0], dtptr->costs[2][2]);

}






