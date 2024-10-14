import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Reaction Time Test')

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CIRCLE_COLOR = (0, 128, 255)

# Font settings
font = pygame.font.Font(None, 36)

# Timing and state variables
reaction_times_appear = []
reaction_times_disappear = []
num_trials = 5
trial_count = 0
stimulus_active = False
stimulus_start_time = 0
user_holding = False
stimulus_disappear_time = 0
disappeared = False
waiting_for_space_release = False

# Random stimulus interval range (seconds)
MIN_DELAY_BETWEEN_TRIALS = 2
MAX_DELAY_BETWEEN_TRIALS = 5

# Random stimulus appear duration range (seconds)
MIN_APPEAR_DURATION = 2
MAX_APPEAR_DURATION = 6

# Function to show text on the screen
def show_text(text, x, y):
    label = font.render(text, True, RED)
    screen.blit(label, (x, y))

# Function to calculate average of a list
def calculate_average(times_list):
    return sum(times_list) / len(times_list) if times_list else 0

def main():
    global stimulus_active, trial_count, user_holding, stimulus_start_time, stimulus_disappear_time, disappeared, waiting_for_space_release
    clock = pygame.time.Clock()
    running = True
    stimulus_delay = random.uniform(MIN_DELAY_BETWEEN_TRIALS, MAX_DELAY_BETWEEN_TRIALS)
    next_stimulus_time = time.time() + stimulus_delay  # Set when the first circle should appear

    while running and trial_count < num_trials:
        screen.fill(WHITE)
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle space bar press when the circle appears
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if stimulus_active and not user_holding and not waiting_for_space_release:  # If the circle is active and user presses space
                    reaction_time = current_time - stimulus_start_time
                    reaction_times_appear.append(reaction_time)
                    user_holding = True
                    print(f"Reaction time to appearance (Trial {trial_count + 1}): {reaction_time:.3f} seconds")

            # Handle space bar release after the circle disappears
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                if not stimulus_active and disappeared and user_holding:  # If the user releases space after the circle disappears
                    reaction_time = current_time - stimulus_disappear_time
                    reaction_times_disappear.append(reaction_time)
                    user_holding = False
                    waiting_for_space_release = False
                    print(f"Reaction time to disappearance (Trial {trial_count + 1}): {reaction_time:.3f} seconds")
                    trial_count += 1  # Move to the next trial
                    if trial_count < num_trials:
                        stimulus_delay = random.uniform(MIN_DELAY_BETWEEN_TRIALS, MAX_DELAY_BETWEEN_TRIALS)
                        next_stimulus_time = current_time + stimulus_delay  # Set time for the next trial

        # Check if it's time to show the stimulus (circle)
        if current_time >= next_stimulus_time and not stimulus_active and not waiting_for_space_release and trial_count < num_trials:
            stimulus_active = True
            stimulus_start_time = current_time  # Record when the circle appears
            stimulus_duration = random.uniform(MIN_APPEAR_DURATION, MAX_APPEAR_DURATION)  # How long the circle stays
            print(f"Circle appeared (Trial {trial_count + 1})")
        
        # If the circle is active, display it and manage its duration
        if stimulus_active:
            pygame.draw.circle(screen, CIRCLE_COLOR, (WIDTH // 2, HEIGHT // 2), 50)

            # Check if the circle should disappear
            if current_time - stimulus_start_time >= stimulus_duration:
                stimulus_disappear_time = current_time
                stimulus_active = False
                disappeared = True  # Mark that the circle has disappeared
                waiting_for_space_release = True  # Now we wait for the user to release the spacebar
                print(f"Circle disappeared (Trial {trial_count + 1})")

        # If trials are complete, calculate and display average times
        if trial_count >= num_trials:
            avg_appear = calculate_average(reaction_times_appear)
            avg_disappear = calculate_average(reaction_times_disappear)
            show_text("Test Complete!", WIDTH // 2 - 100, HEIGHT // 2 - 100)
            print(f"Average reaction time to appearance: {avg_appear:.3f} seconds")
            print(f"Average reaction time to disappearance: {avg_disappear:.3f} seconds")
            pygame.display.flip()
            pygame.time.wait(3000)  # Show results for 3 seconds
            pygame.quit()  # Properly quit Pygame after showing results
            return  # Ensure the program exits after displaying results

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
