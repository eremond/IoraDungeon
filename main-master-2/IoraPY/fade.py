def fadeOut(screen, timer):
    i = 0
    if timer < 256:
        timer = 256
    while i < timer:
        screen.fill((0,0,0))        #use i as transparency counter, look this up later
        i+=1