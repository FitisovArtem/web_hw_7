import my_select as query
import seed
import argparse


def main():
    print('Result select_1:')
    print(query.select_1(), '\n')
    print('Result select_2:')
    print(query.select_2(), '\n')
    print('Result select_3:')
    print(query.select_3(), '\n')
    print('Result select_4:')
    print(query.select_4(), '\n')
    print('Result select_5:')
    print(query.select_5(), '\n')
    print('Result select_6:')
    print(query.select_6(), '\n')
    print('Result select_7:')
    print(query.select_7(), '\n')
    print('Result select_8:')
    print(query.select_8(), '\n')
    print('Result select_9:')
    print(query.select_9(), '\n')
    print('Result select_10:')
    print(query.select_10(), '\n')
    print('Result select_11:')
    print(query.select_11(), '\n')
    print('Result select_12:')
    print(query.select_12(), '\n')


if __name__ == '__main__':
    # main()
    def create(model):
        print(f"Creating entry for {model}.")


    def read(model):
        print(f"Reading entry for {model}.")


    def update(model):
        print(f"Updating entry for {model}.")


    def delete(model):
        print(f"Deleting entry for {model}.")


    def main():
        parser = argparse.ArgumentParser(description="CRUD operations", add_help=False)
        parser.add_argument('-a', '--action', choices=['create', 'list', 'update', 'remove'], required=True,
                            type=str, help='Дія, яку необхідно виконати')
        parser.add_argument('-m', '--model', choices=['Teacher', 'Group', 'Student', 'Subject'], required=True,
                            type=str, help='Клас, який необходно змінити')
        parser.add_argument('-i', '--id', required=False,
                            type=int, help='ID запису, над яким можуть бути виконані дії: ["update", "remove"]')
        parser.add_argument('-n', '--name', required=False,
                            type=str, help='Імʼя запису, над яким можуть бути виконані дії: ["create", "update"]')
        parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                            help='''
                            Приклади:
                            - Створення: -a create -m Group -n NewGroupName
                            - Перегляд:  -a list -m Group
                            - Оновлення: -a update -m Group -i 2 -m NewGroup2
                            - Видалення: -a remove -i 1
                            ''')

        args = parser.parse_args()

        if args.action == 'create':
            if args.name is not None:
                if args.model == 'Group':
                    seed.insert_group(args.name)
                if args.model == 'Teacher':
                    seed.insert_teachers(args.name)
                if args.model == 'Student':
                    seed.insert_students(args.name)
                if args.model == 'Subject':
                    seed.insert_subjects(args.name)

        elif args.action == 'list':
            result = seed.select(args.model)
            for data in result:
                key, value = data
                print("{0}: {1}".format(key, value))

        elif args.action == 'update':
            if args.id is not None and args.name is not None:
                result = seed.update(args.model, args.id, args.name)
                print(result)

        elif args.action == 'remove':
            if args.id is not None:
                result = seed.delete(args.model, args.id)
                print(result)

    main()
