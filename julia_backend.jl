using ZMQ
import JSON

ctx = Context()
recv_socket = Socket(ctx, REQ)
ZMQ.connect(recv_socket, "tcp://127.0.0.1:5556")

function julia_iteration(z, c, maxiter::Int64)
    for n = 1:maxiter
        if abs(z) > 2
            return n-1
        end
        z = z^2 + c
    end
    return maxiter
end

function julia_set(w::Int64, h::Int64, c, maxiter::Int64)
    i::Int64
    j::Int64
    m = Array(Int64, h, w)
    for j=1:h, i=1:w
        z = complex((i-w/2)/(h/2), (j-h/2)/(h/2))
	m[j,i] = julia_iteration(z, c, 256)
    end
    return m
end

function gen_image(key::AbstractString, w::Int64, h::Int64, cre::Float64, cri::Float64, cmap::AbstractString)
    tStart = time()

    tStop = time()
    println("Made ", w, " x ", h, " image in ", tStop, " seconds")
    return
