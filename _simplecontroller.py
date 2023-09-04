import tools
import salescollect
import plotter 
import datacleaning

def main():
    string = input("CPU: ")
    products = salescollect.main(string)

    salescollect.display_product_info(products)

    accepted_conditions_list = ["Used", "Open box"]
    products = datacleaning.filter_products_based_on_condition(products, accepted_conditions_list)

    plotter.plot_distribution(products, string)

main()