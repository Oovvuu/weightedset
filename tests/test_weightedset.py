import pytest
from hypothesis import given
from hypothesis import strategies as st

from weightedset import WeightedSet


class TestAdd:
    """Verify behaviour of add()"""

    @given(key=st.text(), weight=st.floats(min_value=0, exclude_min=True))
    def test_should_add_key_to_empty_set(self, key, weight):
        weights = WeightedSet()
        weights.add(key, weight)
        assert weights[key] == weight

    def test_should_add_new_key_to_nonempty_set(self):
        # Setup
        weights = WeightedSet()
        weights.add("foo", 2.0)

        # Exercise
        weights.add("bar", 3.0)

        # Verify
        assert weights["foo"] == 2.0, "Existing key should not be affected"
        assert weights["bar"] == 3.0, "New key should be stored"

    def test_should_increase_weight_when_key_exists(self):
        # Setup
        weights = WeightedSet()
        weights.add("foo", 2)

        # Exercise
        weights.add("foo", 3)

        # Verify
        assert weights["foo"] == 5

    def test_should_have_nonzero_default_weight(self):
        weights = WeightedSet()
        weights.add("foo")
        assert weights["foo"] > 0

    def test_should_ignore_key_when_weight_is_zero(self):
        weights = WeightedSet()
        weights.add("foo", 0)
        assert "foo" not in weights
        assert (
            weights._weights == {}
        ), "Internal dictionary should not have a copy of the key either"

    def test_should_fail_when_weight_is_negative(self):
        weights = WeightedSet()
        with pytest.raises(ValueError):
            weights.add("foo", -1)


class TestAugmentedTrueDivision:
    """Verify behaviour of the augmented division operator `/=`"""

    def test_should_scale_all_weights(self):
        # Setup
        weights = WeightedSet()
        weights.add("a", 1)
        weights.add("b", 1.0)
        weights.add("c", 17.2)

        # Exercise
        weights /= 2

        # Verify
        assert weights["a"] == 0.5
        assert weights["b"] == 0.5
        assert weights["c"] == 8.6

    def test_should_do_nothing_when_weightedset_is_empty(self):
        weights = WeightedSet()
        weights /= 10

    def test_should_fail_when_scale_is_zero(self):
        # Setup
        weights = WeightedSet()
        weights.add("a", 1.0)

        # Exercise
        with pytest.raises(ZeroDivisionError):
            weights /= 0

    def test_should_fail_when_scale_is_negative(self):
        # Setup
        weights = WeightedSet()
        weights.add("a", 1)

        # Exercise & Verify
        with pytest.raises(ValueError):
            weights /= -3

    def test_should_discard_weights_that_become_zero(self):
        # Setup
        weights = WeightedSet()
        weights.add("a", 1e-200)

        # Exercise
        weights /= 1e200

        # Verify
        assert "a" not in weights

    def test_should_fail_if_any_weight_becomes_infinite_or_nan(self):
        # Setup
        weights = WeightedSet()
        weights.add("a", 1e200)

        # Exercise
        with pytest.raises(OverflowError):
            weights /= 1e-200


class TestAugmentedMultiply:
    """Verify behaviour of the augmented multiply operator `*=`"""

    def test_should_scale_all_weights(self):
        # Setup
        weights = WeightedSet()
        weights.add("a", 1)
        weights.add("b", 1.0)
        weights.add("c", 17.2)

        # Exercise
        weights *= 0.5

        # Verify
        assert weights["a"] == 0.5
        assert weights["b"] == 0.5
        assert weights["c"] == 8.6

    def test_should_do_nothing_when_weightedset_is_empty(self):
        weights = WeightedSet()
        weights *= 10

    def test_should_discard_all_keys_when_scale_is_zero(self):
        # Setup
        weights = WeightedSet()
        weights.add("a", 2)
        weights.add("b", 2.5)

        # Exercise
        weights *= 0

        # Verify
        assert "a" not in weights
        assert "b" not in weights

    def test_should_fail_when_scale_is_negative(self):
        # Setup
        weights = WeightedSet()
        weights.add("a", 1)

        # Exercise & Verify
        with pytest.raises(ValueError):
            weights *= -3

    def test_should_discard_weights_that_become_zero(self):
        # Setup
        weights = WeightedSet()
        weights.add("a", 1e-200)

        # Exercise
        weights *= 1e-200

        # Verify
        assert "a" not in weights

    def test_should_fail_if_any_weight_becomes_infinite_or_nan(self):
        # Setup
        weights = WeightedSet()
        weights.add("a", 1e200)

        # Exercise
        with pytest.raises(ArithmeticError):
            weights *= 1e200


class TestClamp:
    def test_should_reduce_weights_above_maximum(self):
        # Setup
        weights = WeightedSet()
        weights.add("at limit", 5.0)
        weights.add("just above limit", 5.0000001)
        weights.add("way above limit", 57.0)

        # Exercise
        weights.clamp(5.0)

        # Verify
        assert weights["at limit"] == 5.0
        assert weights["just above limit"] == 5.0
        assert weights["way above limit"] == 5.0

    def test_should_not_change_weights_below_maximum(self):
        # Setup
        weights = WeightedSet()
        weights.add("at limit", 5.0)
        weights.add("just below limit", 4.99999999)
        weights.add("well below limit", 1.0)
        weights.add("very small", 0.00001)

        # Exercise
        weights.clamp(5.0)

        # Verify
        assert weights["at limit"] == 5.0
        assert weights["just below limit"] == 4.99999999
        assert weights["well below limit"] == 1.0
        assert weights["very small"] == 0.00001

    def test_should_fail_when_maximum_is_zero(self):
        weights = WeightedSet()
        weights.add("a")
        with pytest.raises(ValueError):
            weights.clamp(0)

    def test_should_fail_when_maximum_is_negative(self):
        weights = WeightedSet()
        weights.add("a")
        with pytest.raises(ValueError):
            weights.clamp(-1)


class TestContains:
    """Verify behaviour of container membership with __contains__()"""

    def test_should_return_true_for_existing_key(self):
        weights = WeightedSet()
        weights.add("foo", 2.0)
        assert "foo" in weights

    def test_should_return_false_when_key_is_missing(self):
        weights = WeightedSet()
        assert "nonexistent" not in weights

    def test_should_return_false_for_existing_value(self):
        # Setup
        weights = WeightedSet()
        weights.add("foo", 2)

        # Exercise & Verify
        assert 2 not in weights
        assert 2.0 not in weights


class TestCopy:
    """Verify behaviour of copy()."""

    def test_should_copy_empty_object(self):
        # Setup
        original = WeightedSet()

        # Exercise
        result = original.copy()

        # Verify
        assert result is not original

        original.add("new_key_in_original")
        assert "new_key_in_original" not in result

        result.add("new_key_in_copy")
        assert "new_key_in_copy" not in original

    def test_should_create_new_set_with_identical_keys(self):
        # Setup
        original = WeightedSet()
        original.add("a", 1)
        original.add("b", 0.000001)
        original.add("c", 1.1)
        original.add("d", 2)
        original.add("e", 10000000.0)
        original.add("f", 3.0)

        # Exercise
        result = original.copy()

        # Verify
        assert result is not original

        assert result.keys() == original.keys()
        for key in result.keys():
            assert result[key] == original[key]
        for key in original.keys():
            assert result[key] == original[key]

        original.add("new_key_in_original")
        assert "new_key_in_original" not in result
        result.add("new_key_in_copy")
        assert "new_key_in_copy" not in original


class TestGetItem:
    """Verify behaviour of container access with __getitem__()"""

    def test_should_get_weight_for_existing_key(self):
        weights = WeightedSet()
        weights.add("foo", 2.0)
        assert weights["foo"] == 2.0

    def test_should_fail_when_key_is_missing(self):
        weights = WeightedSet()
        with pytest.raises(KeyError):
            _ = weights["nonexistent"]


class TestKeys:
    """Verify behaviour of keys()"""

    def test_should_order_keys_by_weight(self):
        # Setup
        weights = WeightedSet()
        weights.add("a", 1)
        weights.add("b", 0.000001)
        weights.add("c", 1.1)
        weights.add("d", 2)
        weights.add("e", 10000000.0)
        weights.add("f", 3.0)

        # Exercise & Verify
        assert weights.keys() == ["e", "f", "d", "c", "a", "b"]


class TestMaxWeights:
    """Verify behaviour of max_weight()"""

    def test_should_return_largest_weight_present(self):
        # Setup
        weights = WeightedSet()
        weights.add("a", 1)
        weights.add("b", 0.000001)
        weights.add("c", 1.1)
        weights.add("d", 2)
        weights.add("e", 10000000.0)
        weights.add("f", 3.0)

        # Exercise & Verify
        assert weights.max_weight() == 10000000.0

    def test_should_return_zero_when_no_keys_present(self):
        weights = WeightedSet()
        assert weights.max_weight() == 0


class TestUpdate:
    """Verify behaviour of update()."""

    def test_should_increase_weights_for_all_keys_from_all_other_sets(self):
        # Setup
        weights = WeightedSet()
        weights.add("a", 1)
        weights.add("b", 2)
        weights.add("c", 3)

        input1 = WeightedSet()
        input1.add("a", 2)
        input1.add("d", 1)
        input1.add("e", 1)

        input2 = WeightedSet()
        input2.add("a", 3)
        input2.add("d", 1.5)
        input2.add("f", 0.9)

        # Exercise
        weights.update(input1, input2)

        # Verify
        assert weights.keys() == ["a", "c", "d", "b", "e", "f"]
        assert weights["a"] == 6
        assert weights["b"] == 2
        assert weights["c"] == 3
        assert weights["d"] == 2.5
        assert weights["e"] == 1
        assert weights["f"] == 0.9

    def test_should_do_nothing_when_other_set_is_empty(self):
        # Setup
        weights = WeightedSet()
        weights.add("a", 1)

        other = WeightedSet()

        # Exercise
        weights.update(other)

        # Verify
        assert weights.keys() == ["a"]
        assert weights["a"] == 1

    def test_should_do_nothing_when_no_other_sets_supplied(self):
        # Setup
        weights = WeightedSet()
        weights.add("a", 1)

        # Exercise
        weights.update()

        # Verify
        assert weights.keys() == ["a"]
        assert weights["a"] == 1

    @pytest.mark.parametrize(
        "other",
        [
            pytest.param(set("a"), id="set"),
            pytest.param([], id="list"),
            pytest.param({"a": 1}, id="dictionary"),
        ],
    )
    def test_should_fail_when_other_object_is_not_weighted_set(self, other):
        # Setup
        weights = WeightedSet()
        weights.add("a", 1)

        # Exercise & Verify
        with pytest.raises(TypeError):
            weights.update(other)
