"""
main.py

single-turn llm call
"""
from llm import ModelInvoker
from dotenv import load_dotenv


load_dotenv()

class Control:
    def __init__(self, model):
        self.model_invoker = ModelInvoker(model, False)

    def start(self, prompt):
        res = self.model_invoker.invoke([{"role": "system", "content": "You will be posed a coding question. Return the answer and only the answer in python."}, {"role": "user", "content": prompt}], [])
        print(res)




PALINDROMIC_OPS = open("problems/palindromic_ops.md").read()
SHADOW_PAIRS = open("problems/shadow_pairs.md").read()
ALTERNATING_SUM_DELETION = open("problems/alternating_sum_deletion.md").read()
MINIMUM_DELETIONS_TO_MAKE_ARRAY_SHARP = open("problems/minimum_deletions_to_make_array_sharp.md").read()
MAXIMUM_PRODUCT_PAIR_WITH_TARGET_SUM = open("problems/maximum_product_pair_with_target_sum.md").read()
REARRANGE_ARRAY_BY_REMOVING_DISTINCT_VALUES = open("problems/rearrange_array_by_removing_distinct_values.md").read()
COUNT_VALUES_WITH_EQUALLY_SPACED_OCCURRENCES_I = open("problems/count_values_with_equally_spaced_occurrences_i.md").read()
CHECK_ASCII_PALINDROMIC = open("problems/check_ascii_palindromic.md").read()
LAST_VISITED_CELL_IN_A_DIRECTIONAL_GRID = open("problems/last_visited_cell_in_a_directional_grid.md").read()
MAXIMUM_EQUAL_ADJACENT_PAIRS_AFTER_AT_MOST_ONE_REPLACEMENT = open("problems/maximum_equal_adjacent_pairs_after_at_most_one_replacement.md").read()
TRANSFORM_ARRAY_USING_PAIR_OPERATIONS = open("problems/transform_array_using_pair_operations.md").read()
COUNT_GOOD_CYCLIC_ROTATIONS = open("problems/count_good_cyclic_rotations.md").read()
K_TH_DIGIT_IN_INFINITE_STRING = open("problems/k_th_digit_in_infinite_string.md").read()

# control = Control("moonshotai/kimi-k3")
control = Control("ibm-granite/granite-4.2-8b")
control.start(MAXIMUM_PRODUCT_PAIR_WITH_TARGET_SUM)