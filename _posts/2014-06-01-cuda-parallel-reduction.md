---
title: "Parallel Reduction w/ NVidia CUDA"
date: 2014-06-01T00:00:00-00:00
last_modified_at: 2014-06-01T00:00:00-00:00
categories:
  - computer architecture
  - school project
permalink: /post-cuda-parallel-reduction/
classes: wide
excerpt: Accelerating via interleaved addressing with NVidia CUDA Framework
header:
  og_image: /images/cuda/0.webp
  teaser: /images/cuda/0.webp
---

![preview](/images/cuda/0.webp){:.align-center}

High Level Overview of the code to follow (heterogeneous programming)

- Prepare memory by copying data from the CPU memory to the GPU memory
- Run the GPU code (kernel) on the GPU until it completes
- Copy back over the results to CPU memory

## Functionally Equivalent Code for CPU only Execution

```c
// naive CPU reduction
float reductionCPU(float* A, int len) {
    float result = 0.0;
    for (int i = 0; i < len ; i++) {
        result += A[i];
    }
    return result;
}
```

## Kernel And Implementation for GPU Execution

```c
// kernel for reduction on GPU
__global__ void reductionKernel(float* A, int len, int level) {
	int thisThreadIndex = blockIdx.x*blockDim.x + threadIdx.x;
	thisThreadIndex = thisThreadIndex * 2 * level;
	if (thisThreadIndex < len) {
		A[thisThreadIndex] = A[thisThreadIndex] + A[thisThreadIndex + level];
	}
}

// Compute reduction of elements in A
// - Result placed in A[0]
// - This code only handles the cases where len is a power of 2 greater than
// or equal to 2^9
void reductionGPU(float* A, int len) {
	// stick with 256 threads_per_block. 
	int threads_per_block = 256; // initially, each block takes care of 512 elements

								 // set an initial number of blocks_per_grid
	int blocks_per_grid = (len / threads_per_block) + 1;

	int level = 1;
	while (level != len) {
		// create 3-dim vector objects to initialize values
		dim3 dim_blocks_per_grid(blocks_per_grid, 1);
		dim3 dim_threads_per_block(threads_per_block, 1, 1);

		// launch kernel on GPU
		reductionKernel<<>>(A, len, level);
		// wait for GPU to finish computation
		cudaThreadSynchronize();

		// scale up level
		level = level * 2;

		// Scale down the number of threads, required to prevent index overflow
		// in the kernel (and the resulting bad memory accesses)
		if (!(blocks_per_grid < 2)) {
			blocks_per_grid = blocks_per_grid / 2;
		}
		else {
			blocks_per_grid = 1;
		}

	}
}
```