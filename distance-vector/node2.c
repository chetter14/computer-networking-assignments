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
} dt2;


/* students to write the following two routines, and maybe some others */

static void notifyNeighboringNodes()
{
	// Send the distance vector to 0, 1, and 3 nodes:
	
	struct rtpkt updatePacket;
	updatePacket.sourceid = 2;
	for (int i = 0; i < 4; ++i)
	{
		updatePacket.mincost[i] = dt2.costs[i][2];
	}
	
	for (int i = 0; i < 4; ++i)
	{
		if (i == 2)
			continue;
		
		updatePacket.destid = i;
		tolayer2(updatePacket);
	}
}

void rtinit2() 
{
	// Initialize a distance vector:
	
	// destination 0:
	dt2.costs[0][0] = 3;
	dt2.costs[0][1] = 999;
	dt2.costs[0][2] = 3;
	dt2.costs[0][3] = 999;
	
	// destination 1:
	dt2.costs[1][0] = 999;
	dt2.costs[1][1] = 1;
	dt2.costs[1][2] = 1;
	dt2.costs[1][3] = 999;
	
	// destination 2:
	dt2.costs[2][0] = 999;
	dt2.costs[2][1] = 999;
	dt2.costs[2][2] = 0;
	dt2.costs[2][3] = 999;
	
	// destination 3:
	dt2.costs[3][0] = 999;
	dt2.costs[3][1] = 999;
	dt2.costs[3][2] = 2;
	dt2.costs[3][3] = 2;
	
	// printf("Node 2 initialization at %f\n\n", clocktime);
	
	printdt2(&dt2);
	
	notifyNeighboringNodes();
}


void rtupdate2(rcvdpkt)
  struct rtpkt *rcvdpkt;
  
{
	int srcNode = rcvdpkt->sourceid;
	
	// iterate over min costs of another node:
	
	printf("\nBefore update:\n");
	printdt2(&dt2);
	
	bool wasUpdated = false;
	for (int i = 0; i < 4; ++i)
	{
		if (dt2.costs[i][2] > rcvdpkt->mincost[i] + dt2.costs[srcNode][2])
		{
			dt2.costs[i][2] = rcvdpkt->mincost[i] + dt2.costs[srcNode][2];
			wasUpdated = true;
		}
	}
	
	// printf("Node 2 update at %f\n\n", clocktime);
	
	if (wasUpdated)
	{
		printf("\nAfter update:\n");
		printdt2(&dt2);
		printf("\nCosts to other nodes: 0 - %d, 1 - %d, 3 - %d\n", dt2.costs[0][2], dt2.costs[1][2], dt2.costs[3][2]);
		notifyNeighboringNodes();
	}
}


printdt2(dtptr)
  struct distance_table *dtptr;
  
{
  printf("                via     \n");
  printf("   D2 |    0     1    3 \n");
  printf("  ----|-----------------\n");
  printf("     0|  %3d   %3d   %3d\n",dtptr->costs[0][0],
	 dtptr->costs[0][1],dtptr->costs[0][3]);
  printf("dest 1|  %3d   %3d   %3d\n",dtptr->costs[1][0],
	 dtptr->costs[1][1],dtptr->costs[1][3]);
  printf("     3|  %3d   %3d   %3d\n",dtptr->costs[3][0],
	 dtptr->costs[3][1],dtptr->costs[3][3]);
}






