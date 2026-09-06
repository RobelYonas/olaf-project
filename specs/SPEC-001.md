# Spec-001: Adaptive Braking Deceleration Policy

The emergency brake system shall initiate deceleration when time-to-collision is below 1.5 seconds.
If sensor confidence drops below 80 percent, the controller must degrade gracefully to manual override.
The target deceleration rate must not exceed 9.8 m/s^2 under dry pavement conditions.
