import time
import threading
import subprocess

from pyplayground.client.RobotThymio2 import RobotThymio2
from pyplayground.client.RobotEPuck import RobotEPuck

"""
Robot thymio2:
    Sensores de Proximidad:
        0: frontal izquierdo izquierdo
        1: frontal izquierdo
        2: frontal frontal
        3: frontal derecho
        4: frontal derecho derecho
        5: trasero izquierdo
        6: trasero derecho
    Sensores de línea:
        0: izquierdo
        1: derecho

Robot epuck  :
    Sensores de Proximidad:
        0: frontal frontal derecho
        1: frontal derecho
        2: derecho
        3: trasero derecho
        4: trasero izquierdo
        5: izquierdo
        6: frontal izquierdo
        7: frontal frontal izquierdo
"""

# Requiere servidor en el playground "simple.world"
class TestSensorsThreads():
    def __init__( self ):
        pass

    def run( self ):
        # levantamos el playground en otro proceso
        try:
            #pg = subprocess.Popen( [ "python", "-m", "pyplayground.server.Playground", "../worlds/simple.world" ], shell=False )
            time.sleep( 1 )
        except Exception as e:
            print( e )
            exit()

        # los datos de conexion al playground
        host = "127.0.0.1"
        port = 44444

        # creanos los robots
        thymio = MyThymio2( "Thymio-01", host, port )     # tiene 7 sensores de proximidad
        epuck  = MyEPuck( "Epuck-01", host, port )        # tiene 8 sensores de proximidad

        # los levantamos en hilos separados
        threading.Thread( target=thymio.run, args=(), name="Thymio-01" ).start()
        threading.Thread( target=epuck.run , args=(), name="Epuck-01"  ).start()

        # loop clasico
        t = time.time()
        while( time.time() - t < 20 ):
            time.sleep( 1 )

        # detenemos los robots
        thymio.finish()
        epuck.finish()

        # detenemos el playground
        #pg.send_signal( subprocess.signal.SIGTERM )


class MyThymio2( RobotThymio2 ):
    def __init__( self, name, host, port ):
        super().__init__( name, host, port )
        self.running = False
        self.me = None
        self.s = 20

    def run( self ):
        self.me = threading.current_thread()
        self.setSpeed( self.s, self.s )
        self.running = True
        while(self.running ):
            self.getSensors()
            distancia = self.proximitySensorDistances[2]
            if( distancia < 3 ):
                self.setSpeed( -self.s*10, self.s )
                time.sleep( 1 )
                self.setSpeed( self.s, self.s )
        self.setSpeed( 0, 0 )
        self.close()

    def finish( self ):
        self.running = False
        self.me.join()
        self.close()

class MyEPuck( RobotEPuck ):
    def __init__( self, name, host, port ):
        super().__init__( name, host, port )
        self.running = False
        self.me = None
        self.s = 10

    def run( self ):
        self.me = threading.current_thread()
        self.setSpeed( self.s, self.s )
        self.running = True
        while(self.running ):
            self.getSensors()
            distanciaR = self.proximitySensorDistances[0]
            distanciaL = self.proximitySensorDistances[7]
            if( distanciaL < 4 or distanciaR < 4 ):
                self.setSpeed( -self.s*10, self.s )
                time.sleep( 1 )
                self.setSpeed( self.s, self.s )
        self.setSpeed( 0, 0 )
        self.close()

    def finish( self ):
        self.running = False
        self.me.join()
        self.close()


# show time
TestSensorsThreads().run()
