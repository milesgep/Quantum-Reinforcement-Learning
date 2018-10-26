from qiskit import QuantumProgram

#################### Grover Iteration for 1 qubit

#Is it possible?


#################### Grover Iteration for 2 qubits

def gIteration00(qc, qr):
  # apply the s gate to both qubits
  qc.s(qr)

  # apply h gate to the 2nd qubit
  qc.h(qr[1])

  # apply CNOT with control as 2nd qubit to target as 1st qubit
  qc.cx(qr[0], qr[1])

  # apply h gate to the 2nd qubit again
  qc.h(qr[1])

  # apply the s gate to both qubits
  qc.s(qr)

  # add the H gate in the Qubit 0 and 1
  qc.h(qr)

  # now use the X gate
  qc.x(qr)

  # apply h gate to the 2nd qubit again
  qc.h(qr[1])

  # apply CNOT with control as 2nd qubit to target as 1st qubit
  qc.cx(qr[0], qr[1])

  # apply h gate to the 2nd qubit again
  qc.h(qr[1])

  # now use the X gate
  qc.x(qr)

  # add the H gate in the Qubit 0 and 1
  qc.h(qr)

  return qc, qr
#########################################################

def gIteration01(qc, qr):
  # apply the s gate to 1st qubit
  qc.s(qr[0])

  # apply h gate to the 2nd qubit
  qc.h(qr[1])

  # apply CNOT with control as 2nd qubit to target as 1st qubit
  qc.cx(qr[0], qr[1])

  # apply h gate to the 2nd qubit again
  qc.h(qr[1])

  # apply the s gate to 1st qubit
  qc.s(qr[0])

  # add the H gate in the Qubit 0 and 1
  qc.h(qr)

  # now use the X gate
  qc.x(qr)

  # apply h gate to the 2nd qubit again
  qc.h(qr[1])

  # apply CNOT with control as 2nd qubit to target as 1st qubit
  qc.cx(qr[0], qr[1])

  # apply h gate to the 2nd qubit again
  qc.h(qr[1])

  # now use the X gate
  qc.x(qr)

  # add the H gate in the Qubit 0 and 1
  qc.h(qr)

  return qc, qr

def gIteration10(qc, qr):
  # apply the s gate to both qubits
  qc.s(qr[1])

  # apply h gate to the 2nd qubit
  qc.h(qr[1])

  # apply CNOT with control as 2nd qubit to target as 1st qubit
  qc.cx(qr[0], qr[1])

  # apply h gate to the 2nd qubit again
  qc.h(qr[1])

  # apply the s gate to both qubits
  qc.s(qr[1])

  # add the H gate in the Qubit 0 and 1
  qc.h(qr)

  # now use the X gate
  qc.x(qr)

  # apply h gate to the 2nd qubit again
  qc.h(qr[1])

  # apply CNOT with control as 2nd qubit to target as 1st qubit
  qc.cx(qr[0], qr[1])

  # apply h gate to the 2nd qubit again
  qc.h(qr[1])

  # now use the X gate
  qc.x(qr)

  # add the H gate in the Qubit 0 and 1
  qc.h(qr)

  return qc, qr

def gIteration11(qc, qr):
  # apply h gate to the 2nd qubit
  qc.h(qr[1])

  # apply CNOT with control as 2nd qubit to target as 1st qubit
  qc.cx(qr[0], qr[1])

  # apply h gate to the 2nd qubit again
  qc.h(qr[1])

  # add the H gate in the Qubit 0 and 1
  qc.h(qr)

  # now use the X gate
  qc.x(qr)

  # apply h gate to the 2nd qubit again
  qc.h(qr[1])

  # apply CNOT with control as 2nd qubit to target as 1st qubit
  qc.cx(qr[0], qr[1])

  # apply h gate to the 2nd qubit again
  qc.h(qr[1])

  # now use the X gate
  qc.x(qr)

  # add the H gate in the Qubit 0 and 1
  qc.h(qr)

  return qc, qr

#################### Grover Iteration for 3 qubits

def gIteration000(qc, qr):

  return qc, qr

def gIteration001(qc, qr):
  
  return qc, qr

def gIteration010(qc, qr):
  
  return qc, qr

def gIteration011(qc, qr):
  
  return qc, qr

def gIteration100(qc, qr):
  
  return qc, qr

def gIteration101(qc, qr):
  
  return qc, qr

def gIteration110(qc, qr):
  
  return qc, qr

def gIteration111(qc, qr):
  
  return qc, qr

###########################################################
"""
if __name__ == '__main__':

  Q_program = QuantumProgram()
  Q_program1 = QuantumProgram()

  qr = Q_program.create_quantum_register("qr", 2)
  cr = Q_program.create_classical_register("cr", 2)
  qc = Q_program.create_circuit("superposition", [qr], [cr])

  qr1 = Q_program1.create_quantum_register("qr", 2)
  cr1 = Q_program1.create_classical_register("cr", 2)
  qc1 = Q_program1.create_circuit("superposition", [qr1], [cr1])

  # put the qubits into a superposition of the states
  qc.h(qr)

  qc, qr = gIteration00(qc, qr)
  #qc.measure(qr, cr)

  qc, qr = gIteration01(qc, qr)
  qc, qr = gIteration01(qc, qr)
  qc, qr = gIteration01(qc, qr)
  #qc.measure(qr, cr)

  qc, qr = gIteration10(qc, qr)
  qc, qr = gIteration10(qc, qr)
  qc, qr = gIteration10(qc, qr)
  qc, qr = gIteration10(qc, qr)
  qc, qr = gIteration10(qc, qr)

  # Copy the contents of the quantum register
  qr1 = qr

  qc.measure(qr, cr)

  # Compiled and execute in the local_qasm_simulator

  result = Q_program.execute(["superposition"], backend='local_qasm_simulator', shots=1)

  # Show the results
  print(result)
  print(result.get_data("superposition"))
  classical_state = result.get_data("superposition")['classical_state']


  #Use Grover Iteration on the 2nd register based on the outcome of measuring the first
  if(classical_state == 0):
    qc1, qr1 = gIteration00(qc1, qr1)
  elif(classical_state == 1):
    qc1, qr1 = gIteration01(qc1, qr1)
  elif(classical_state == 2):
    qc1, qr1 = gIteration10(qc1, qr1)
  elif(classical_state == 3):
    qc1, qr1 = gIteration11(qc1, qr1)

  qc1.measure(qr1, cr1)
  result1 = Q_program1.execute(["superposition"], backend='local_qasm_simulator', shots=1)

  print(result1)
  print(result1.get_data("superposition"))

  """