## Summary

To successfully downsample the inputted pointcloud, I sought to explore the application of an octree and how it's used to partition 3D point cloud space. My main understanding came from [this article.](http://www.open3d.org/docs/latest/tutorial/geometry/octree.html)

I tried to follow the conventional process, starting by representing the entire space as one node and recursively adding child nodes based off of boundaries, then traversing the octree, calculating the average of each node as processed, and then reading it back to the node. Finally, each averaged node's value is added to the output and written to a CSV.

One caveat I'd mention is that the load time is roughly 10 seconds on average for a maximum octree depth of 7, so optimization would need to be further explored in the future.

See `downsampler.ipynb` for visualization of the input and output! The first successful run downsampled from 350k+ points to ~30k points.