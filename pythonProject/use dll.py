import clr


clr.AddReference(r"C:\Users\adity\PycharmProjects\pythonProject\dll\CalcProject.dll")

#or

#dll_path = r"C:\Users\adity\PycharmProjects\pythonProject\dll\CalcProject.dll"
#import sys
#sys.path.append(assembly_path)


from CalcProject import calculate

obj = calculate()

print(obj.Add(1, 2))