def rider_name(part_of_rider_heat_results): 
    """Preprocesses a drivers name by eliminating replacements and appends the name to the final dict"""
    if part_of_rider_heat_results[2].text.find('\n'):
        rider_name = part_of_rider_heat_results[2].text[part_of_rider_heat_results[2].text.find('\n')+1:]
    else:
        rider_name = part_of_rider_heat_results[2].text

    return rider_name