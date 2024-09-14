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

struct distance_table 
{
  int costs[4][4];
} dt0;


/* students to write the following two routines, and maybe some others */

void notifyNeighboringNodes()
{
	// Send the distance vector to 1, 2, and 3 nodes:
	
	struct rtpkt updatePacket;
	updatePacket.sourceid = 0;
	for (int i = 0; i < 4; ++i)
	{
		updatePacket.mincost[i] = dt0.costs[i][0];
	}
	
	for (int i = 1; i < 4; ++i)
	{
		updatePacket.destid = i;
		tolayer2(updatePacket);
	}
}

void rtinit0() 
{
	// Initialize a distance vector:
	
	// destination 0:
	dt0.costs[0][0] = 0;
	dt0.costs[0][1] = 999;		// source 0 and dest 0 through 1/2/3 makes no sense, so assign "infinity"
	dt0.costs[0][2] = 999;
	dt0.costs[0][3] = 999;
	
	// destination 1:
	dt0.costs[1][0] = 1;
	dt0.costs[1][1] = 999;
	dt0.costs[1][2] = 999;		// unknown
	dt0.costs[1][3] = 999;		// unknown
	
	// destination 2:
	dt0.costs[2][0] = 3;
	dt0.costs[2][1] = 999;		// unknown
	dt0.costs[2][2] = 999;
	dt0.costs[2][3] = 999;		// unknown
	
	// destination 3:
	dt0.costs[3][0] = 7;
	dt0.costs[3][1] = 999;		// unknown
	dt0.costs[3][2] = 999;		// unknown
	dt0.costs[3][3] = 999;
	
	printdt0(&dt0);
	
	notifyNeighboringNodes();
}

// it seems that the rtupdate() function better to make parameterized 
// and use 1 function for all the nodes (because the code is almost identical)

void rtupdate0(rcvdpkt)
  struct rtpkt *rcvdpkt;
{
	int srcNode = rcvdpkt->sourceid;
	
	// iterate over min costs of another node:
	
	bool wasUpdated = false;
	for (int i = 0; i < 4; ++i)
	{
		if (dt0.costs[i][0] > rcvdpkt->mincost[i] + dt0.costs[srcNode][0])
		{
			dt0.costs[i][0] = rcvdpkt->mincost[i] + dt0.costs[srcNode][0];
			wasUpdated = true;
		}
	}
	
	if (wasUpdated)
		notifyNeighboringNodes();
}


printdt0(dtptr)
  struct distance_table *dtptr;
  
{
  printf("                via     \n");
  printf("   D0 |    1     2    3 \n");
  printf("  ----|-----------------\n");
  printf("     1|  %3d   %3d   %3d\n",dtptr->costs[1][1],
	 dtptr->costs[1][2],dtptr->costs[1][3]);
  printf("dest 2|  %3d   %3d   %3d\n",dtptr->costs[2][1],
	 dtptr->costs[2][2],dtptr->costs[2][3]);
  printf("     3|  %3d   %3d   %3d\n",dtptr->costs[3][1],
	 dtptr->costs[3][2],dtptr->costs[3][3]);
}

linkhandler0(linkid, newcost)   
  int linkid, newcost;

/* called when cost from 0 to linkid changes from current value to newcost*/
/* You can leave this routine empty if you're an undergrad. If you want */
/* to use this routine, you'll need to change the value of the LINKCHANGE */
/* constant definition in prog3.c from 0 to 1 */
	
{
}
