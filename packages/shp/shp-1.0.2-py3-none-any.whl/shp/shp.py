from shp.compiler.Compiler import Compiler
from shp.Watchdog import Watchdog
from time import sleep

class SHP:
  def __init__(self, source, target):
    self.compiler = Compiler(source)
    self.watchdog = Watchdog(lambda: self.onUpdate())
    self.source = source
    self.target = target

  def compile(self):
    print('[SHP] Compiling', self.target)
    html = self.compiler.compile()
    with open(self.target, 'w') as file:
      file.write(html)

  def watch(self, noBlock=False):
    self.onUpdate()
    if not noBlock: self.run()

  def onUpdate(self):
    self.compile()
    self.watchdog.updateWatchList([self.source] + self.compiler.includedFiles)

  def stop(self):
    print('[SHP] Interrupted')
    self.watchdog.stopAll()

  def run(self):
    print('[SHP] Press Ctrl+C to stop')
    try:
      while True:
        sleep(.1)
    except KeyboardInterrupt:
      self.stop()
