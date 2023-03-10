from register import *


class Process:
    __states = ['ready', 'running', 'blocked']

    def __init__(self, p_id: str, commands: list, os):
        self.__process_id = p_id
        self.__context = {'ir': ('', -sys.maxsize), 'acc': -sys.maxsize, 'temp': -sys.maxsize,
                          'current_line': -sys.maxsize}
        self.__state = '-'
        self.__commands = commands

        self.__start_line = len(os.ram)
        self.__end_pc = self.__start_line + len(commands)
        self.__current_line = 0

    def run(self, signal: str, os, pc: PC, ir: IR, acc: Accumulator, temp: Temp):

        if signal == 'create_process':
            self.__state = Process.__states[0]
            os.add_process(self)
            os.send_to_ram(self)

        if signal == 'run_process' and self.__state != Process.__states[2]:
            self.__state = Process.__states[1]

            pc.set(self.__current_line + self.__start_line)

            instruction, value = os.ram[f'{self.__process_id} {self.__current_line}'].split()
            ir.set(instruction, int(value))

            acc.set(self.__context['acc'])

            if os.type_instruction(instruction) == 'store':
                os.store_operate(int(value), temp, acc)

            if os.type_instruction(instruction) == 'arithmetic':
                os.arithmetic_operate(int(value), instruction, temp, acc)

            self.__current_line += 1

            self.__context['ir'] = (instruction, value)
            self.__context['acc'] = acc.get()
            self.__context['temp'] = temp.get()
            self.__context['current_line'] = self.__current_line

        if signal == 'block_process':
            self.__state = Process.__states[2]
            ir.reset()
            acc.reset()
            temp.reset()
            pc.reset()

        if signal == 'unblock_process':
            self.__state = Process.__states[1]

            ir_value = self.__context['ir']
            acc_value = self.__context['acc']
            temp_value = self.__context['temp']
            current_line = self.__context['current_line']

            ir.set(ir_value[0], ir_value[1])
            acc.set(acc_value)
            temp.set(temp_value)
            self.__current_line = current_line

        if signal == 'show_context':
            result = self.get_id() + '\n' + 'Instruction Register:' + str(self.__context['ir']) +\
                      '\n\n' + 'Accumulator:' + str(self.__context['acc']) + '\t' + \
                      f'Temp:' + str(self.__context['temp']) + '\n' +\
                      'pc: ' + str(self.__start_line + self.__current_line) + '\t\t\t' + \
                      'State:' + self.__state

            result = '--------------------------------\n' + result + '\n--------------------------------\n'
            print(result)

        if signal == "kill_process":
            self.__context = {'ir': ('', -sys.maxsize), 'acc': -sys.maxsize, 'temp': -sys.maxsize,
                              'current_line': -sys.maxsize}
            ir.reset()
            acc.reset()
            temp.reset()
            os.kill_process(self.__process_id)

    def get_id(self):
        return self.__process_id

    def get_commands(self):
        return self.__commands
