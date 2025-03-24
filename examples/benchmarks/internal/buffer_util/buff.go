package buffer_util

type BufferPool struct {
	buffers    chan int // Channel acts as a semaphore
	pool       [][]byte // Slice to store the actual buffers
	bufferSize int      // Size of each buffer
}

// NewBufferPool creates a new buffer pool with the specified number of buffers
// and buffer size.
func NewBufferPool(numBuffers, bufferSize int) *BufferPool {
	pool := &BufferPool{
		buffers:    make(chan int, numBuffers), // Buffered channel for semaphore
		pool:       make([][]byte, numBuffers), // Pre-allocate the buffers
		bufferSize: bufferSize,
	}

	// Initialize the buffers in the pool
	for i := 0; i < numBuffers; i++ {
		pool.pool[i] = make([]byte, bufferSize) // Allocate each buffer
		pool.buffers <- i
	}
	return pool
}

// GetBuffer retrieves a buffer from the pool. It blocks until a buffer is available.
func (bp *BufferPool) GetBuffer() ([]byte, int) {
	buffer_id := <-bp.buffers // Receive from channel, blocking if empty (semaphore wait)
	return bp.pool[buffer_id], buffer_id
}

// returns a buffer to the pool, making it available for other goroutines.
func (bp *BufferPool) ReleaseBuffer(buffer_id int) {
	bp.buffers <- buffer_id // Send to channel, releasing the semaphore
}
