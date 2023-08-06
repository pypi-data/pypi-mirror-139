
import py2D

win = py2D.Screen_([1200,750])

i=0

m = py2D.Sub_.Mouse()



while win.CLOSE():
    win.Update().SETBGCOLOR(); win.SETFPS(60)
    cube = win.f2D.Rect('red',[300,300],[i+1,i*2],0,win.screen)
    i+=0.05
    cube.Rotate(i)
    cube.Draw()
    
    
    
            
        
    

    
    
    
    