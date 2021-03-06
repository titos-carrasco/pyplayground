import time
import random
import subprocess

from pyplayground.client.RobotThymio2 import RobotThymio2
from pyplayground.client.RobotEPuck import RobotEPuck

# Requiere servidor en el playground "simple.world"
class TestLed():
    def __init__( self ):
        pass

    def run( self ):
        # Levantamos el playground en otro procesos
        try:
            #pg = subprocess.Popen( [ "python", "-m", "pyplayground.server.Playground", "../worlds/simple.world" ], shell=False )
            time.sleep( 1 )
        except Exception as e:
            print( e )
            exit()

        # Los datos de conexion al playground
        host = "127.0.0.1"
        port = 44444

        # Usamos try/except para conocer los errores que se produzcan
        try:
            # Accesamos los robots y configuramos algunos de sus atributos
            thymio = RobotThymio2( "Thymio-01", host, port )
            leds = [0]*23
            ledval = 0

            epuck  = RobotEPuck( "Epuck-01" , host, port )

            # Loop clasico
            t = time.time()
            ledval = 0
            while( time.time() - t < 5 ):
                epuck.setLedRing( ledval )
                for i in range(3,23): leds[ i ] = ledval
                thymio.setLedsIntensity( leds )
                ledval = 0 if ledval == 1 else 1
                time.sleep( 0.5 )

            thymio.close()
            epuck.close()
        except ConnectionResetError:
            print( "Conexion abortada" )
        except Exception as e:
            print( e )

        # Detenemos el playground
        #pg.send_signal( subprocess.signal.SIGTERM )


# show time
TestLed().run()
