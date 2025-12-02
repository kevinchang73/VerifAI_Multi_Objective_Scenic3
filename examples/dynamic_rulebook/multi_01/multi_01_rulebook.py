import numpy as np

from verifai.rulebook import rulebook

class rulebook_multi01(rulebook):
    iteration = 0

    def __init__(self, graph_path, rule_file, save_path=None, single_graph=False, using_sampler=-1, exploration_ratio=2.0):
        rulebook.using_sampler = using_sampler
        rulebook.exploration_ratio = exploration_ratio
        super().__init__(graph_path, rule_file, single_graph=single_graph)
        self.save_path = save_path

    def evaluate(self, traj):
        # Extract trajectory information
        positions = np.array(traj.result.trajectory)
        init_lane_coords = np.array(traj.result.records["initLaneCoords"])
        left_lane_coords = np.array(traj.result.records["leftLaneCoords"])
        ego_is_in_init_lane = np.array(traj.result.records["egoIsInInitLane"])
        ego_is_in_left_lane = np.array(traj.result.records["egoIsInLeftLane"])

        # Find switching points
        switch_idx_1 = len(traj.result.trajectory)
        switch_idx_2 = len(traj.result.trajectory)
        distances_to_obs = positions[:, 0, :] - positions[:, 1, :]
        distances_to_obs = np.linalg.norm(distances_to_obs, axis=1)
        for i in range(len(distances_to_obs)):
            if distances_to_obs[i] < 8.5 and switch_idx_1 == len(traj.result.trajectory):
                switch_idx_1 = i
                continue
            if distances_to_obs[i] > 10 and switch_idx_1 < len(traj.result.trajectory) and switch_idx_2 == len(traj.result.trajectory):
                switch_idx_2 = i
                break
        assert switch_idx_1 < len(traj.result.trajectory), "Switching point 1 cannot be found"
        
        # Evaluation
        indices_0 = np.arange(0, switch_idx_1)
        indices_1 = np.arange(switch_idx_1, switch_idx_2)
        indices_2 = np.arange(switch_idx_2, len(traj.result.trajectory))
        if self.single_graph:
            rho0 = self.evaluate_segment(traj, 0, indices_0)
            rho1 = self.evaluate_segment(traj, 0, indices_1)
            rho2 = self.evaluate_segment(traj, 0, indices_2)
            print('Actual rho:')
            print(rho0[0], rho0[1])
            print(rho1[0], rho1[1])
            print(rho2[0], rho2[1])
            rho = self.evaluate_segment(traj, 0, np.arange(0, len(traj.result.trajectory)))
            return np.array([rho])
        rho0 = self.evaluate_segment(traj, 0, indices_0)
        rho1 = self.evaluate_segment(traj, 1, indices_1)
        rho2 = self.evaluate_segment(traj, 2, indices_2)
        return np.array([rho0, rho1, rho2])