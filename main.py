import func

#  Просим ввести код посылки
barcode = input('Введите код посылки: ')  #  RJ042664964RU
print('\n[^] Получаю данные о посылке...\n')


#  Получаем данные о посылке исходя из введенного кода
parselInfo = func.getParsel(barcode)

#  Выводим название посылки и ее примерную дату получения
print('[*] Посылка: %s\n[!] %s\n\n' %
      (parselInfo['Name'], parselInfo['GetDate']))

#  Выводим все операции с посылкой
for i in reversed(range(0, len(parselInfo['Operations']))):
    print('[#] ', parselInfo['Operations'][i])