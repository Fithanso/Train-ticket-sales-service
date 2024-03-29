class IncrementingSeatNamesCreator:
    def __init__(self, train_entity):
        self.train = train_entity

        self.seats_in_wagon = 0

        self.start_seats_count_from = 1
        self.stop_seats_count_on = 0
        self.seats_count_step = 1

        self.start_wagons_count_from = 1
        self.stop_wagons_count_on = 0
        self.wagons_count_step = 1

    def get_incrementing_seat_numbers(self) -> dict:
        # method generates numbers (place names) and assigns them to wagons
        # numbers differ from wagon to wagon, so they are generated with offset

        self.__create_initial_calculation_data()

        seats_divided_by_wagons = {}

        for wagon_number in self.__get_wagons_iterator():
            wagon_number = str(wagon_number)
            seat_numbers = [str(seat_number) for seat_number in self.__get_seats_iterator()]

            self.__shift_iteration_indent()

            is_bc = wagon_number in self.train.bc_wagons_numbers
            seats_divided_by_wagons[wagon_number] = {'seat_numbers': seat_numbers,
                                                     'is_bc_wagon': is_bc}

        return seats_divided_by_wagons

    def __shift_iteration_indent(self):
        self.start_seats_count_from += self.seats_in_wagon
        self.stop_seats_count_on += self.seats_in_wagon

    def __get_wagons_iterator(self):
        return range(self.start_wagons_count_from, self.stop_wagons_count_on, self.wagons_count_step)

    def __get_seats_iterator(self):
        return range(self.start_seats_count_from, self.stop_seats_count_on, self.seats_count_step)

    def __create_initial_calculation_data(self):
        self.seats_in_wagon = self.train.total_seats // self.train.wagons_number

        self.stop_seats_count_on = self.seats_in_wagon + self.start_seats_count_from
        self.stop_wagons_count_on = self.train.wagons_number + self.start_wagons_count_from
