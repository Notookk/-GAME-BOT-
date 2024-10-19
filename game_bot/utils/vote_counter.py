from collections import defaultdict

class VoteCounter:
    def __init__(self):
        self.votes = defaultdict(int)

    def reset(self):
        """Resets the vote counts."""
        self.votes.clear()

    def cast_vote(self, voter_id: int, voted_player_id: int):
        """Records a vote from one player to another."""
        self.votes[voted_player_id] += 1

    def get_majority_vote(self) -> int | None:
        """Returns the player ID with the majority vote or None."""
        if not self.votes:
            return None
        max_votes = max(self.votes.values())
        candidates = [p for p, v in self.votes.items() if v == max_votes]
        return candidates[0] if len(candidates) == 1 else None
