// ---- Core JS ----
import.meta.glob('./**/*.js', { eager: true });

// ---- Module JS ----
import.meta.glob('../../../modules/*/assets/js/**/*.js', { eager: true });

// ---- Core CSS ----
import.meta.glob('../css/**/*.css', { eager: true });

// ---- Module CSS ----
import.meta.glob('../../../modules/*/assets/css/**/*.css', { eager: true });
