import numpy as np

class Update:
    def __init__(self):
        pass

    def _update(self, p: dict, gbest_params: dict):
        for p_item, g_item in zip(p.items(), gbest_params.items()):
            parameter = p_item[0]
            g_values = g_item[1]
            p_values = p_item[1][0]

            # Calculate steps only if values are numeric
            if type(g_values) not in [str, np.str_]:
                rev_iter = [r for r in reversed(range(1, self.n_iter + 1))]
                displacement = (g_values - p_values) / rev_iter[self.iter]
                displacement = displacement * self.iter
                p[parameter] = p_values + displacement
                if type(p_values) in [int, np.int64]:
                    p[parameter] = [int(p[parameter])]

            # Set values to string if gbest is string
            else:
                p[parameter] = [g_values]

        return p