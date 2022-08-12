---
title: "Weighted Vector Addition w/ NVidia CUDA"
date: 2014-06-01T00:00:00-00:00
last_modified_at: 2014-06-01T00:00:00-00:00
categories:
  - computer architecture
  - school project
permalink: /post-cuda-weighted-vector-addition/
classes: wide
excerpt: Accelerating vector addition w/ NVidia CUDA framework
header:
  og_image: /images/cuda/preview.jpg
  teaser: /images/cuda/preview.jpg
---

High Level Overview of the code to follow (heterogeneous programming)

- Prepare memory by copying data from the CPU memory to the GPU memory
- Run the GPU code (kernel) on the GPU until it completes
- Copy back over the results to CPU memory

## Functionally Equivalent Code for CPU only Execution

```c
// compute weighted vector addition on CPU: out = weight_a*A + weight_b*B
void cpuWeightedVectorAdd(float* out, float* A, float* B, int len, float weight_a, float weight_b) {
	for (int i = 0; i < len; i++) {
		out[i] = A[i] * weight_a + B[i] * weight_b;
	}
}
```

## Kernel And Implementation for GPU Execution

```c
// kernel for weighted vector addition on GPU
__global__ void weightedVecAddKernel(float* out, float* A, float* B, int len, float weight_a, float weight_b) {
	int thisThreadIndex = blockIdx.x*blockDim.x + threadIdx.x;
	if (thisThreadIndex < len) {
		out[thisThreadIndex] = A[thisThreadIndex] * weight_a + B[thisThreadIndex] * weight_b;
	}
}
// compute weighted vector addition on GPU: out = weight_a*A + weight_b*B
void weightedVecAdd(float* out, float* A, float* B, int len, float weight_a, float weight_b) {
	// figures out how to fit computation to the "geometry"
	// of the GPU. Stick with the max 512 threads_per_block and then
	// compute the right number of blocks_per_grid to compute the entire addition
	int threads_per_block = 512;
	int blocks_per_grid = (len / threads_per_block) + 1;
	printf("Blocks in a grid: %d\n", blocks_per_grid);

	// 3-dim vector objects to initialize values
	dim3 dim_blocks_per_grid(blocks_per_grid, 1);
	dim3 dim_threads_per_block(threads_per_block, 1, 1);

	// launch kernel on GPU
	weightedVecAddKernel<<>>(out, A, B, len, weight_a, weight_b);

	// wait for GPU to finish computation
	cudaThreadSynchronize();
}
```