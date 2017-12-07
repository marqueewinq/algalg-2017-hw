"""
    Solution for https://stepik.org/lesson/59290/step/7?unit=36810
"""

def read_prices():
    """
        Reads prices as declared task
    """
    n_prices = int(input())
    price = []
    for _ in range(n_prices):
        price.append(int(input()))
    return price


def read_edges():
    """
        Reads edges as declared in task
    """
    n_edges = int(input())
    edges = []
    for _ in range(n_edges):
        src, dst = map(int, input().split())
        edges.append([src, dst])
    return edges


def main():
    """
        Solver as in http://web.cs.iastate.edu/~cs511/handout10/Approx_VC.pdf
    """
    prices = read_prices()
    edges = read_edges()

    for edge in edges:
        src, dst = edge
        if prices[src] == 0 or prices[dst] == 0:
            continue
        prices[src] -= min(prices[src], prices[dst])
        prices[dst] -= min(prices[src], prices[dst])
    print(" ".join([str(vtx) for vtx, price in enumerate(prices) if price == 0]))

if __name__ == '__main__':
    main()
