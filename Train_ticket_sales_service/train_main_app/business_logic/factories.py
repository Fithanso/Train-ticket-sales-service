
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

    def get_incrementing_seat_names(self) -> dict:
        self.seats_in_wagon = self.train.total_seats // self.train.wagons_number

        self.__create_data_for_incr_calculation()

        seats_divided_by_wagons = {}

        for wagon_number in self.__get_wagons_iterator():
            wagon_number = str(wagon_number)
            seat_names = [str(seat_name) for seat_name in self.__get_seats_iterator()]

            self.__shift_iteration_indent()

            is_bc = wagon_number in self.train.bc_wagons_numbers
            seats_divided_by_wagons[wagon_number] = {'seat_names': seat_names,
                                                     'is_bc_wagon': is_bc}

        return seats_divided_by_wagons

    def __shift_iteration_indent(self):
        self.start_seats_count_from += self.seats_in_wagon
        self.stop_seats_count_on += self.seats_in_wagon

    def __get_wagons_iterator(self):
        return range(self.start_wagons_count_from, self.stop_wagons_count_on, self.wagons_count_step)

    def __get_seats_iterator(self):
        return range(self.start_seats_count_from, self.stop_seats_count_on, self.seats_count_step)

    def __create_data_for_incr_calculation(self):

        self.stop_seats_count_on = self.seats_in_wagon + self.start_seats_count_from
        self.stop_wagons_count_on = self.train.wagons_number + self.start_wagons_count_from