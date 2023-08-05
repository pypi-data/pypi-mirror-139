#pragma once

#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/components/touchscreen/touchscreen.h"
#include "esphome/core/component.h"
#include "esphome/core/helpers.h"

namespace esphome {
namespace touchscreen {

class TouchscreenBinarySensor : public binary_sensor::BinarySensor,
                                public Component,
                                public TouchListener,
                                public Parented<Touchscreen> {
 public:
  void setup() override { this->parent_->register_listener(this); }

  /// Set the touch screen area where the button will detect the touch.
  void set_area(int16_t x_min, int16_t x_max, int16_t y_min, int16_t y_max) {
    this->x_min_ = x_min;
    this->x_max_ = x_max;
    this->y_min_ = y_min;
    this->y_max_ = y_max;
  }

  void touch(TouchPoint tp) override;
  void release() override;

 protected:
  int16_t x_min_, x_max_, y_min_, y_max_;
};

}  // namespace touchscreen
}  // namespace esphome
