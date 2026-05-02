def calculate_reward(build_time, cost, success):

    failure_penalty = 0 if int(success) == 1 else 100

    reward = -(0.6 * build_time + 0.3 * cost + 0.1 * failure_penalty)

    return reward


def estimate_cost(build_time, compute_type):

    cost_map = {
        "BUILD_GENERAL1_SMALL": 1,
        "BUILD_GENERAL1_MEDIUM": 2,
        "BUILD_GENERAL1_LARGE": 4
    }

    return build_time * cost_map.get(compute_type, 1)