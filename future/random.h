#ifndef __RANDOM_H
#define __RANDOM_H

#include <random>

namespace rnd {

struct Generator {

    std::mt19937 gen;

    template <typename T>
    void init(T seed) {
        gen.seed(seed);
    }

    template <typename T>
    T range(T a, T b) {
        std::uniform_int_distribution<T> dist(a, b);
        return dist(gen);
    }

    template <typename T>
    T gauss(T mean, T stddev) {
        std::normal_distribution<T> dist(mean, stddev);
        return dist(gen);
    }
};

inline Generator& get() {
    static Generator ret;
    return ret;
}

}

#endif
