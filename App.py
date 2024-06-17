class App():
    def __init__(self):
        self.visa_required = {
            'CCS': False,
            'AUA': True,
            'BON': True,
            'CUR': True,
            'SXM': True,
            'SDQ': False,
            'SBH': False,
            'POS': False,
            'BGI': False,
            'FDF': False,
            'PTP': False
        }

    def start(self):
        print('Hello, world!')
        print('Visa required for SXM:', self.visa_required['SXM'])

        while True:
            print('Enter "exit" to quit.')
            user_input = input('Enter a country code: ')
            if user_input == 'exit':
                break
            print('Visa required:', self.visa_required[user_input])
