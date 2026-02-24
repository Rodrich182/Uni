# Ejercicio 0 - warmup.py
#
# TinyVM.
#
# La máquina tiene 8 registros (R0..R7) y las siguientes instrucciones:
#
# ('ADD', 'Ra', 'Rb', 'Rd') -> Rd = Ra + Rb
# ('SUB', 'Ra', 'Rb', 'Rd') -> Rd = Ra - Rb
# ('MOV', valor, 'Rd')      -> Rd = valor
# ('LD', 'Rs', 'Rd', off)   -> Rd = MEMORIA[ Rs + off ]
# ('ST', 'Rs', 'Rd', off)   -> MEMORIA[ Rd + off ] = Rs
# ('JMP', 'Rd', off)        -> PC = Rd + off
# ('BZ',  'Rt', off)        -> si Rt == 0: PC = PC + off
# ('HALT',)                 -> Detiene la máquina
#
# Nota: en la implementación original la instrucción aparece como BRZ; aquí
# se acepta BZ y BRZ (BZ es un alias).

class Halt(Exception):
    pass


class TinyVM(object):
    def run(self, memory):
        '''
        Run a program. memory is a Python list containing the program
        instructions and other data. Upon startup, all registers are
        initialized to 0. R7 is initialized with the highest valid
        memory address.
        '''
        self.pc = 0
        self.registers = {f'R{d}': 0 for d in range(8)}
        self.memory = memory
        self.registers['R7'] = len(memory) - 1
        try:
            while True:
                op, *args = self.memory[self.pc]
                self.pc += 1
                getattr(self, op)(*args)
        except Halt:
            self.registers = {key: 0 for key in self.registers}
        return

    def ADD(self, ra, rb, rd):
        self.registers[rd] = self.registers[ra] + self.registers[rb]

    def SUB(self, ra, rb, rd):
        self.registers[rd] = self.registers[ra] - self.registers[rb]

    def MOV(self, value, rd):
        self.registers[rd] = value

    def LD(self, rs, rd, offset):
        self.registers[rd] = self.memory[self.registers[rs] + offset]

    def ST(self, rs, rd, offset):
        self.memory[self.registers[rd] + offset] = self.registers[rs]

    def JMP(self, rd, offset):
        self.pc = self.registers[rd] + offset

    def BRZ(self, rt, offset):
        if not self.registers[rt]:
            self.pc += offset

    # Alias para que también funcione ('BZ', ...)
    def BZ(self, rt, offset):
        return self.BRZ(rt, offset)

    def HALT(self):
        raise Halt()


machine = TinyVM()

# ------------------------------------------------------------
# Problema 1: Computadoras
# Usando TinyVM, calcular 2 + 3 - 4.

prog1 = [
    ('MOV', 2, 'R1'),
    ('MOV', 3, 'R2'),
    ('ADD', 'R1', 'R2', 'R3'),   # R3 = 2 + 3
    ('MOV', 4, 'R4'),
    ('SUB', 'R3', 'R4', 'R5'),   # R5 = (2+3) - 4
    ('ST', 'R5', 'R7', 0),       # MEM[R7] = R5 (última celda)
    ('HALT',),
    0                            # Resultado
]

machine.run(prog1)
print('Resultado del programa 1:', prog1[-1], '(debería ser 1)')


# ------------------------------------------------------------
# Problema 2: Computación
# Escribir un programa TinyVM que calcule 23 * 37 (sin multiplicación).

prog2 = [
    ('MOV', 23, 'R1'),           # multiplicando
    ('MOV', 37, 'R2'),           # multiplicador (contador)
    ('MOV', 0,  'R3'),           # acumulador
    ('MOV', 1,  'R4'),           # constante 1
    ('BRZ', 'R2', 3),            # si R2==0 saltar a ST (fin)
    ('ADD', 'R3', 'R1', 'R3'),   # acc += 23
    ('SUB', 'R2', 'R4', 'R2'),   # R2 -= 1
    ('JMP', 'R0', 4),            # volver al BRZ (R0==0)
    ('ST', 'R3', 'R7', 0),       # guardar resultado
    ('HALT',),
    0                            # Resultado
]

machine.run(prog2)
print('Resultado del programa 2:', prog2[-1], f'(El resultado es {23*37})')


# ------------------------------------------------------------
# Problema 3: Abstracción
# Implementar mul(x,y) que calcule x*y en TinyVM.
# Los inputs se guardan al final del programa y se leen con LD.

def mul(x, y):
    prog = [
        ('LD',  'R7', 'R1', -2),     # R1 = x   (penúltimo-1)
        ('LD',  'R7', 'R2', -1),     # R2 = y   (penúltimo)
        ('MOV', 0,    'R3'),         # acc = 0
        ('MOV', 1,    'R4'),         # const 1
        ('BRZ', 'R2', 3),            # si y==0 -> guardar
        ('ADD', 'R3', 'R1', 'R3'),   # acc += x
        ('SUB', 'R2', 'R4', 'R2'),   # y -= 1
        ('JMP', 'R0', 4),            # loop
        ('ST',  'R3', 'R7', 0),      # resultado
        ('HALT',),
        x,                           # Input 1
        y,                           # Input 2
        0                            # Resultado
    ]
    machine.run(prog)
    return prog[-1]


print(f'Problema 3: 51 * 53 = {mul(51, 53)}. El resultado es {51*53}.')


# ------------------------------------------------------------
# Problema 4: Desafío
# Reescribir fib recursivo como un único programa TinyVM.
# Implementación: simulación de recursión con pila explícita en memoria.
#
# Frame en la pila: [n, temp, stage]
# - stage=0: evaluar fib(n)
# - stage=1: ya calculado fib(n-1) en retval; falta fib(n-2)
# - stage=2: ya calculado fib(n-2) en retval; sumar temp(=fib(n-1)) y devolver


def fib(n):
    if n <= 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def _build_fib_prog(n, stack_cells=1200):
    code = []
    labels = {}
    fixups = []  # (idx, kind, label)

    def label(name):
        labels[name] = len(code)

    def emit(op, *args):
        code.append((op, *args))

    def brz(rt, target_label):
        idx = len(code)
        emit('BRZ', rt, 0)
        fixups.append((idx, 'BRZ', target_label))

    def jmp0(target_label):
        idx = len(code)
        emit('JMP', 'R0', 0)
        fixups.append((idx, 'JMP', target_label))

    # Registros:
    # R0 = 0 (no tocar)
    # R1 = n
    # R2 = stage / scratch
    # R3 = temp / scratch
    # R4 = retval
    # R5 = 1 (const)
    # R6 = SP
    # R7 = result_addr (lo inicializa la VM)

    emit('LD',  'R7', 'R1', -1)        # R1 = n (input)
    emit('MOV', 'STACK_BASE', 'R6')    # R6 = SP = stack_base (parcheado)
    emit('MOV', 0, 'R4')               # retval = 0
    emit('MOV', 1, 'R5')               # const1 = 1

    # push initial frame: [n,0,0]
    emit('ST',  'R1', 'R6', 0); emit('ADD', 'R6', 'R5', 'R6')
    emit('MOV', 0, 'R3')
    emit('ST',  'R3', 'R6', 0); emit('ADD', 'R6', 'R5', 'R6')
    emit('ST',  'R3', 'R6', 0); emit('ADD', 'R6', 'R5', 'R6')

    label('LOOP')
    emit('MOV', 'STACK_BASE', 'R2')
    emit('SUB', 'R6', 'R2', 'R2')      # R2 = SP - stack_base
    brz('R2', 'EXIT')                  # si vacío, salir

    # pop stage, temp, n
    emit('SUB', 'R6', 'R5', 'R6'); emit('LD', 'R6', 'R2', 0)  # stage
    emit('SUB', 'R6', 'R5', 'R6'); emit('LD', 'R6', 'R3', 0)  # temp
    emit('SUB', 'R6', 'R5', 'R6'); emit('LD', 'R6', 'R1', 0)  # n

    brz('R2', 'STAGE0')                # stage==0
    emit('SUB', 'R2', 'R5', 'R2')      # stage-1
    brz('R2', 'STAGE1')                # stage==1

    label('STAGE2')
    emit('ADD', 'R4', 'R3', 'R4')      # retval += temp
    jmp0('LOOP')

    label('STAGE1')
    # push frame (n, temp=retval, stage=2)
    emit('ST', 'R1', 'R6', 0); emit('ADD', 'R6', 'R5', 'R6')
    emit('ADD', 'R4', 'R0', 'R3')      # temp = retval
    emit('ST', 'R3', 'R6', 0); emit('ADD', 'R6', 'R5', 'R6')
    emit('MOV', 2, 'R2')
    emit('ST', 'R2', 'R6', 0); emit('ADD', 'R6', 'R5', 'R6')

    # push child (n-2, 0, 0)
    emit('MOV', 2, 'R2')
    emit('SUB', 'R1', 'R2', 'R2')      # n-2
    emit('ST', 'R2', 'R6', 0); emit('ADD', 'R6', 'R5', 'R6')
    emit('MOV', 0, 'R3')
    emit('ST', 'R3', 'R6', 0); emit('ADD', 'R6', 'R5', 'R6')
    emit('ST', 'R3', 'R6', 0); emit('ADD', 'R6', 'R5', 'R6')
    jmp0('LOOP')

    label('STAGE0')
    # base si n==1 o n==2 (asumiendo n>=1)
    emit('SUB', 'R1', 'R5', 'R2')      # n-1
    brz('R2', 'BASE')
    emit('MOV', 2, 'R2')
    emit('SUB', 'R1', 'R2', 'R2')      # n-2
    brz('R2', 'BASE')

    # push parent (n,0,1)
    emit('ST', 'R1', 'R6', 0); emit('ADD', 'R6', 'R5', 'R6')
    emit('MOV', 0, 'R3')
    emit('ST', 'R3', 'R6', 0); emit('ADD', 'R6', 'R5', 'R6')
    emit('MOV', 1, 'R2')
    emit('ST', 'R2', 'R6', 0); emit('ADD', 'R6', 'R5', 'R6')

    # push child (n-1,0,0)
    emit('SUB', 'R1', 'R5', 'R2')      # n-1
    emit('ST', 'R2', 'R6', 0); emit('ADD', 'R6', 'R5', 'R6')
    emit('MOV', 0, 'R3')
    emit('ST', 'R3', 'R6', 0); emit('ADD', 'R6', 'R5', 'R6')
    emit('ST', 'R3', 'R6', 0); emit('ADD', 'R6', 'R5', 'R6')
    jmp0('LOOP')

    label('BASE')
    emit('MOV', 1, 'R4')
    jmp0('LOOP')

    label('EXIT')
    emit('ST', 'R4', 'R7', 0)
    emit('HALT',)

    # Resolver saltos
    for idx, kind, target in fixups:
        target_idx = labels[target]
        op = code[idx][0]
        if kind == 'JMP':
            code[idx] = (op, 'R0', target_idx)
        elif kind == 'BRZ':
            offset = target_idx - (idx + 1)  # PC ya incrementado
            code[idx] = (op, code[idx][1], offset)
        else:
            raise RuntimeError(kind)

    # stack_base = índice justo después del HALT (o sea, len(code))
    stack_base = len(code)
    patched = []
    for ins in code:
        if ins[0] == 'MOV' and ins[1] == 'STACK_BASE':
            patched.append(('MOV', stack_base, ins[2]))
        else:
            patched.append(ins)

    # Memoria final: código + pila + [n, resultado]
    return patched + [0] * stack_cells + [n, 0]


def fib_vm(n):
    # Para respetar exactamente el fib() dado (n<=2 -> 1) sin depender de
    # comparaciones de signo dentro de TinyVM.
    if n <= 2:
        return 1

    prog = _build_fib_prog(n)
    machine.run(prog)
    return prog[-1]


print(f'Problema 4: fib_vm(10) = {fib_vm(10)} (fib(10) = {fib(10)})')

# AUTOR: Rodrigo Pelayo Lopez