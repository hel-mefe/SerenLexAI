import { useForm } from '@tanstack/react-form'
import { FormInput } from './FormInput'
import { PasswordInput } from './PasswordInput'
import { PrimaryButton } from './PrimaryButton'
import { AuthDivider } from './AuthDivider'
import { authStorage } from '@/lib/auth.storage'
import { useNavigate } from 'react-router-dom'

export function SignInForm() {
    const navigate = useNavigate() ;

    const form = useForm({
    defaultValues: {
        email: '',
        password: '',
    },
    onSubmit: async ({ value }) => {
        if (
            value.email === 'Muhammad' &&
            value.password === 'Muhammad'
        ) {
            authStorage.login()
            navigate('/dashboard/overview')
        } else {
            alert('Invalid credentials')
        }
        }
    })

  return (
    <div className="flex-1 flex items-center justify-center px-10 pb-6">
      <div className="w-full max-w-[340px]">
        <h2 className="text-3xl font-bold text-neutral-900 mb-6">
          Sign In
        </h2>

        <form
          onSubmit={(e) => {
            e.preventDefault()
            e.stopPropagation()
            form.handleSubmit()
          }}
        >
          <form.Field
            name="email"
            validators={{
              onChange: ({ value }) =>
                !value
                  ? 'Email is required'
                  : undefined,
            }}
          >
            {(field) => (
              <FormInput
                label="Email or Username"
                field={field}
                placeholder="you@company.com"
              />
            )}
          </form.Field>

          <form.Field
            name="password"
            validators={{
              onChange: ({ value }) =>
                value.length < 6
                  ? 'Password must be at least 6 characters'
                  : undefined,
            }}
          >
            {(field) => (
              <PasswordInput field={field} />
            )}
          </form.Field>

          <PrimaryButton>
            Sign In
          </PrimaryButton>
        </form>

        <AuthDivider />
      </div>
    </div>
  )
}