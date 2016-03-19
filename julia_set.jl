using PyPlot

function julia(z, maxiter::Int64)
    # c=-0.8+0.156im
    c = 0.3 + 0.023im
    for n = 1:maxiter
        if abs(z) > 2
            return n-1
        end
        z = z^2 + c
    end
    return maxiter
end

# create a 1000x500 Array for our picture
h = 1000
w = 1000
m = Array(Int64, h, w)
  
# time measurements
print("starting...\n")
tStart=time()
  
# for every pixel
for y=1:h, x=1:w
    # translate numbers [1:w, 1:h] -> -2:2 + -1:1 im
    c = complex((x-w/2)/(h/2), (y-h/2)/(h/2))
    # call our julia function
    m[y,x] = julia(c, 256)
end
  
tStop = time()
print("done. took ", tStop-tStart, " seconds\n");

# write the ppm-file
imshow(m, cmap=ColorMap("Blues"))

show()
