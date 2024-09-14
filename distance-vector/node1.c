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

int connectcosts1[4] = { 1,  0,  1, 999 };

struct distance_table 
{
  int costs[4][4];
} dt1;


/* students to write the following two routines, and maybe some others */

static void notifyNeighboringNodes()
{
	// Send the distance vector to 0 and 2 nodes:
	
	struct rtpkt updatePacket;
	updatePacket.sourceid = 1;
	for (int i = 0; i < 4; ++i)
	{
		updatePacket.mincost[i] = dt1.costs[i][1];
	}
	
	for (int i = 0; i < 4; ++i)
	{
		if (i == 1 || i == 3)
			continue;
		
		updatePacket.destid = i;
		tolayer2(updatePacket);
	}
}

rtinit1() 
{
	// Initialize a distance vector:
	
	// destination 0:
	dt1.costs[0][0] = 1;
	dt1.costs[0][1] = 1;
	dt1.costs[0][2] = 999;
	dt1.costs[0][3] = 999;
	
	// destination 1:
	dt1.costs[1][0] = 999;
	dt1.costs[1][1] = 0;
	dt1.costs[1][2] = 999;
	dt1.costs[1][3] = 999;
	
	// destination 2:
	dt1.costs[2][0] = 999;
	dt1.costs[2][1] = 1;
	dt1.costs[2][2] = 1;
	dt1.costs[2][3] = 999;
	
	// destination 3:
	dt1.costs[3][0] = 999;
	dt1.costs[3][1] = 999;
	dt1.costs[3][2] = 999;
	dt1.costs[3][3] = 999;
	
	// printf("Node 1 initialization at %f\n\n", clocktime);
	
	printdt1(&dt1);
	
	notifyNeighboringNodes();
}


rtupdate1(rcvdpkt)
  struct rtpkt *rcvdpkt;
  
{
	int srcNode = rcvdpkt->sourceid;
	
	// iterate over min costs of another node:
	
	printf("\nBefore update:\n");
	printdt1(&dt1);
	
	bool wasUpdated = false;
	for (int i = 0; i < 4; ++i)
	{
		if (dt1.costs[i][1] > rcvdpkt->mincost[i] + dt1.costs[srcNode][1])
		{
			dt1.costs[i][1] = rcvdpkt->mincost[i] + dt1.costs[srcNode][1];
			wasUpdated = true;
		}
	}
	
	// printf("Node 1 update at %f\n\n", clocktime);
	
	if (wasUpdated)
	{
		printf("\nAfter update:\n");
		printdt1(&dt1);
		printf("\nCosts to other nodes: 0 - %d, 2 - %d, 3 - %d\n", dt1.costs[0][1], dt1.costs[2][1], dt1.costs[3][1]);
		notifyNeighboringNodes();
	}
}


printdt1(dtptr)
  struct distance_table *dtptr;
  
{
  printf("             via   \n");
  printf("   D1 |    0     2 \n");
  printf("  ----|-----------\n");
  printf("     0|  %3d   %3d\n",dtptr->costs[0][0], dtptr->costs[0][2]);
  printf("dest 2|  %3d   %3d\n",dtptr->costs[2][0], dtptr->costs[2][2]);
  printf("     3|  %3d   %3d\n",dtptr->costs[3][0], dtptr->costs[3][2]);

}



linkhandler1(linkid, newcost)   
int linkid, newcost;   
/* called when cost from 1 to linkid changes from current value to newcost*/
/* You can leave this routine empty if you're an undergrad. If you want */
/* to use this routine, you'll need to change the value of the LINKCHANGE */
/* constant definition in prog3.c from 0 to 1 */
	
{
}

